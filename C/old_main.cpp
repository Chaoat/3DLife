#include <irrlicht.h>
#include <driverChoice.h>
#include <iostream>
#include <Python.h>
#include <stdexcept>
// #include "EventReceiver.h"

// #pragma comment(lib, "Irrlicht.lib")

using namespace irr;

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

int main()
{
    // std::cout << "Start" << std::endl;

    /*************************************
     * Initialize the Python Interpreter *
     *************************************/

    // Start the Python interpreter
    Py_Initialize();

    // Add the folder where test.py is located to python path
    PyRun_SimpleString("import sys\n");
    PyRun_SimpleString("sys.path.append(\"/home/kikai/Documents/FIT2083/3DLife/C\")");

    // creates a new reference to test module
    // so we have to DECREF it in EndPython()
    pName = PyUnicode_FromString("test");

    // Import the python module test.py. New reference.
    pModule = PyImport_Import(pName);
    if(pModule==NULL) {
        //no module found or there was an error when compiling python code
        PyErr_Print();
        printf("Could not load the python module \"test\"\n");
        return EndPython(); 
    }

    // Borrow a reference to the module's dict
    // No decref
    pDict = PyModule_GetDict(pModule);
    if (!pDict) {
        PyErr_Print();
        throw std::runtime_error("Could not get dict for the python module \"test\"");
    }

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

    // pValue is the return of test function
    // arguments are null
    pValue = PyObject_CallObject(pFunc, NULL);
    if (!pValue) {
        PyErr_Print();
        throw std::runtime_error("Did not receive a list after calling \"getState\"");
    }

    std::cout << "C++: Size of the python list: " << PyList_Size(pValue) << std::endl;

    // https://stackoverflow.com/questions/35141827/python-c-api-transfer-a-pyobject-into-c-array

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

    // MyEventReceiver receiver;
    // device->setEventReceiver(&receiver);

    video::IVideoDriver* driver = device->getVideoDriver();
    scene::ISceneManager* smgr = device->getSceneManager();

    // the thing we want to look at
    scene::ISceneNode* box = smgr->addCubeSceneNode();
    // disable lighting for box
    box->setMaterialFlag(video::EMF_LIGHTING, false);

    // add camera
    scene::ICameraSceneNode* cam = smgr->addCameraSceneNode(box);
    cam->setTarget( box->getAbsolutePosition() );


//    // add a dynamic light
//    smgr->addLightSceneNode(0, core::vector3df(-20, 0, 0), video::SColorf(1.f, 0.f, 0.f, 1.f));
//    smgr->addLightSceneNode(0, core::vector3df(0, -20, 0), video::SColorf(0.f, 1.f, 0.f, 1.f)); 
//    smgr->addLightSceneNode(0, core::vector3df(0, 0, -20), video::SColorf(0.f, 0.f, 1.f, 1.f));

    // set up angles for orbital camera
    f32 Radius = 20.f;
    f32 Theta  = 180.f; // degrees
    f32 Phi    = 90.f; // degrees

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
            // if (receiver.Keys[KEY_NUMPAD1])
            //     Radius -= (LinearVelocity * deltaTime);
            // if (receiver.Keys[KEY_NUMPAD3])
            //     Radius += (LinearVelocity * deltaTime);
            // if (receiver.Keys[KEY_NUMPAD4])
            //     Theta += (AngularVelocity * deltaTime);
            // if (receiver.Keys[KEY_NUMPAD6])
            //     Theta -= (AngularVelocity * deltaTime);
            // if (receiver.Keys[KEY_NUMPAD8])
            //     Phi += (AngularVelocity * deltaTime);
            // if (receiver.Keys[KEY_NUMPAD2])
            //     Phi -= (AngularVelocity * deltaTime);
            // if (receiver.Keys[KEY_NUMPAD5])
            // {
            //     Theta = 180.f;
            //     Phi   = 90.f;
            // }

            // prevent camera from walking into our box
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

            // camera is a child of the cube, so our offset is actually
            // the position of the camera
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