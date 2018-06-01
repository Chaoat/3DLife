#include <irrlicht.h>
#include <driverChoice.h>
#include <iostream>
#include <string>
#include <Python.h>
#include <stdexcept>

#include <stdio.h>  /* defines FILENAME_MAX */
#ifdef WINDOWS
    #include <direct.h>
    #define GetCurrentDir _getcwd
#else
    #include <unistd.h>
    #define GetCurrentDir getcwd
#endif

using namespace irr;

class MyEventReceiver : public IEventReceiver {
public:
    // This is the one method that we have to implement
    virtual bool OnEvent(const SEvent& event)
    {
        // Remember whether each key is down or up
        if (event.EventType == EET_KEY_INPUT_EVENT) {
            KeyIsDown[event.KeyInput.Key] = event.KeyInput.PressedDown;
            // std::cout << "key " << event.KeyInput.Key;
            // if (event.KeyInput.PressedDown)
            //     std::cout << " down";
            // else
            //     std::cout << " up";
            // std::cout << std::endl;
        }
        return false;
    }

    // This is used to check whether a key is being held down
    virtual bool IsKeyDown(EKEY_CODE keyCode) const
    {
        return KeyIsDown[keyCode];
    }
    
    MyEventReceiver()
    {
        for (u32 i=0; i<KEY_KEY_CODES_COUNT; ++i)
            KeyIsDown[i] = false;
    }

private:
    // We use this array to store the current state of each key
    bool KeyIsDown[KEY_KEY_CODES_COUNT];
};

void PrintInstructions(){

    std::cout << "\nWelcome to 3DLife!\n\n";

    std::cout << "Controls\n" 
        << "------------------------\n" 
        << "Orbit Left   " << "Left arrow" << "\n" 
        << "Orbit Up     " << "Up arrow" << "\n" 
        << "Orbit Right  " << "Right arrow" << "\n" 
        << "Orbit Down   " << "Down arrow" << "\n" 
        << "Zoom Out     " << "Plus key" << "\n" 
        << "Zoom In      " << "Minus key" << "\n" 
        << "Reset Camera " << "Right Shift" << "\n" 
        // << "desc" << "key" << "\n" 
        << std::endl;
}

void Py_ImportParentDirectory(std::string dir) {

    PyRun_SimpleString("import sys\n");

    char cCurrentPath[FILENAME_MAX];
    if (!GetCurrentDir(cCurrentPath, sizeof(cCurrentPath))) {
        std::cout << "GetCurrentDir Failed!\n";
        std::cout << errno << "\n";
        exit(1);
    }
    cCurrentPath[sizeof(cCurrentPath) - 1] = '\0'; /* not really required */
    // printf ("The current working directory is %s\n", cCurrentPath);

    std::string sCurrentPath(cCurrentPath);

    std::size_t slash = sCurrentPath.rfind("/");
    std::string sParentPath = sCurrentPath.substr(0, slash+1);

    std::string full = "sys.path.append(\"" + sParentPath + dir + "\")";

    std::cout << "Importing python module: " + sParentPath + dir << "\n";
    // call the python string sys.path.append("../dir")
    PyRun_SimpleString(full.c_str());
}

PyObject *pName, *pModule, *pDict, *pFunc, *pValue, *pArgs, *pClass, *pInstance;

int EndPython() {
    // Destroy references to python objects so they can be garbage collected
    // using XDECREF instead of DECREF to avoid problems is pInstance is NULL

    Py_XDECREF(pInstance); 
    Py_XDECREF(pValue);
    Py_XDECREF(pModule);
    Py_XDECREF(pName);
    
    // Stop the Python Interpreter
    Py_Finalize();
    
    return 1;
}

int main(int argc, char *argv[]){

    /*************************************
     * Initialize the Python Interpreter *
     *************************************/

    // Start the Python interpreter
    Py_Initialize();

    // Add the folder where python file is located to python path
    Py_ImportParentDirectory("c-python");

    // create a reference to name of python module
    pName = PyUnicode_FromString("pythonTest");

    // Import the python module and create a reference to it 
    pModule = PyImport_Import(pName);
    if(pModule==NULL) {
        //no module found or there was an error when compiling python code
        PyErr_Print();
        printf("Could not load the python module \"test\"\n");
        return EndPython(); 
    }

    // Borrow a reference to the module's dict
    pDict = PyModule_GetDict(pModule);

    // borrow a reference to get_state function
    pFunc = PyDict_GetItemString(pDict, "get_state");
    if(pFunc==NULL) {
        printf("No such function get_state\n");
        return EndPython();
    } else if (!PyCallable_Check(pFunc)) {
        PyErr_Print();
        printf("get_state is not callable!\n");
        return EndPython();
    }

    // get the return value of the test function
    // arguments are NULL
    pValue = PyObject_CallObject(pFunc, NULL);
    
    // printf("Size of the c++ list is: %ld\n", PyList_Size(pValue));
    
    /*******************
     * Set up Irrlicht *
     *******************/   

    // ask user to select driver
    video::E_DRIVER_TYPE driverType = driverChoiceConsole();

    // start up the engine
    IrrlichtDevice *device = createDevice(driverType,
        core::dimension2d<u32>(640,480));
    if (device == 0)
        return 1; // could not create selected driver.

    // Set up keyboard input
    MyEventReceiver receiver;
    device->setEventReceiver(&receiver);

    video::IVideoDriver* driver = device->getVideoDriver();
    scene::ISceneManager* smgr = device->getSceneManager();

    // add a cube
    scene::ISceneNode* box = smgr->addCubeSceneNode();
    // disable lighting for cube
    box->setMaterialFlag(video::EMF_LIGHTING, false);

    // add camera
    scene::ICameraSceneNode* cam = smgr->addCameraSceneNode(box);
    cam->setTarget( box->getAbsolutePosition() );

    PrintInstructions();

    // set up angles for orbital camera
    f32 Radius = 20.f;  // zoom
    f32 Theta  = 180.f; // lat degrees
    f32 Phi    = 90.f;  // long degrees

    f32 LinearVelocity = 20.f;
    f32 AngularVelocity = 40.f;

    u32 lastFrameTime = device->getTimer()->getRealTime();

    while(device->run())
    {
        // calculate deltaTime time as fractional seconds
        u32 now = device->getTimer()->getRealTime();
        f32 deltaTime = (now - lastFrameTime) / 1000.f;
        lastFrameTime = now;

        // window is active, so render scene
        if (device->isWindowActive())
        {
            if (driver->beginScene(true, true, video::SColor(255, 100, 100, 140)))
            {
                smgr->drawAll();

                driver->endScene();
            }

            // adjust camera position based on current key input
            if (receiver.IsKeyDown(KEY_PLUS))
                Radius -= (LinearVelocity * deltaTime);
            if (receiver.IsKeyDown(KEY_MINUS))
                Radius += (LinearVelocity * deltaTime);
            if (receiver.IsKeyDown(KEY_LEFT))
                Theta += (AngularVelocity * deltaTime);
            if (receiver.IsKeyDown(KEY_RIGHT))
                Theta -= (AngularVelocity * deltaTime);
            if (receiver.IsKeyDown(KEY_DOWN))
                Phi += (AngularVelocity * deltaTime);
            if (receiver.IsKeyDown(KEY_UP))
                Phi -= (AngularVelocity * deltaTime);
            if (receiver.IsKeyDown(KEY_RSHIFT))
            {
                // reset rotation and zoom
                Theta  = 180.f;
                Phi    = 90.f;
                Radius = 20.f;
            }

            // restrict maximum zoom
            if (Radius < 10.f)
                Radius = 10.f;

            // lame ass gimble lock prevention. if you don't want to do this
            // you need to adjust the up vector of the camera so it never is
            // parallel to the look at vector
            if (Phi < 10.f)
                Phi = 10.f;
            else if (170.f < Phi)
                Phi = 170.f;

            f32 sinOfPhi = sinf(Phi * core::DEGTORAD);
            f32 cosOfPhi = cosf(Phi * core::DEGTORAD);

            f32 sinOfTheta = sinf(Theta * core::DEGTORAD);
            f32 cosOfTheta = cosf(Theta * core::DEGTORAD);

            core::vector3df offset;

            offset.X = Radius * sinOfTheta * sinOfPhi;
            offset.Y = Radius * cosOfPhi;
            offset.Z = Radius * cosOfTheta * sinOfPhi;

            // camera is a child of the cube, so our offset is 
            // actually the position of the camera
            cam->setPosition(offset);
            cam->setTarget( box->getAbsolutePosition() );
            cam->updateAbsolutePosition();
        }
    }

    /************
     * Clean up *
     * **********/
    
    EndPython();
    
    // drop the graphics device
    device->drop();

    return 0;
}