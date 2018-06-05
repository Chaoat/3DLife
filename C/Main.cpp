#include <irrlicht.h>
#include <driverChoice.h>
#include <iostream>
#include <string>
#include <Python.h>
#include <stdexcept>
#include <cmath>
#include <vector>

#include "TransferData.h"
#include <boost/interprocess/mapped_region.hpp>
#include <boost/interprocess/file_mapping.hpp>

#ifdef WINDOWS
    #include <boost/interprocess/windows_shared_memory.hpp>
    #define OS_SHARED_MEM boost::interprocess::windows_shared_memory
    #include <direct.h>
    #define GetCurrentDir _getcwd
    #include <windows.h>
#else
    #include <boost/interprocess/shared_memory_object.hpp>
    #define OS_SHARED_MEM boost::interprocess::shared_memory_object
    #include <unistd.h>
    #define GetCurrentDir getcwd
#endif

using namespace irr;

boost::interprocess::file_mapping m_file;
boost::interprocess::mapped_region region;
TransferData* data;

IrrlichtDevice *device;
video::IVideoDriver* driver;
scene::ISceneManager* smgr;
scene::IMeshManipulator* meshman;

scene::ICameraSceneNode* cam;
scene::ISceneNode* cameraPivot;
scene::IMeshSceneNode* highlight;
video::SColor highlightColor(255, 255, 0, 0);
f32 highlightScale = 1.2f;

// initial angles for orbital camera
f32 camRadius = 20.f;  // zoom
f32 camTheta  = 180.f; // lat degrees
f32 camPhi    = 90.f;  // long degrees
f32 camLinearVelocity  = 20.f;
f32 camAngularVelocity = 40.f;

u32 lastFrameTime = 0;
u32 now;
f32 deltaTime;

unsigned int numCells, numDimensions, numLayers;
std::vector<scene::IMeshSceneNode*> cells;
std::vector<unsigned int> gridPositions;
float cellSize = 1;
unsigned int drawLayer = 0;
bool drawMode = false;

void selectCell(unsigned int cell) {
    // TODO: implement cell state modifications

    std::cout << "Selected cell " << cell << "\n";
}

class MyEventReceiver : public IEventReceiver {
public:

    // store info on mouse state
    struct SMouseState
    {
        core::position2di Position;
        bool LeftButtonDown;
        SMouseState() : LeftButtonDown(false) { }
    } MouseState;

    virtual bool OnEvent(const SEvent& event)
    {
        // Remember whether each key is down or up
        if (event.EventType == EET_KEY_INPUT_EVENT) {
            KeyIsDown[event.KeyInput.Key] = event.KeyInput.PressedDown;

            // Do something on keyup / keydown
            if (event.KeyInput.Key == KEY_KEY_D && event.KeyInput.PressedDown) {
                drawMode = !drawMode;
            } else if (event.KeyInput.Key == KEY_COMMA && event.KeyInput.PressedDown) {
                if (drawLayer > 0)
                    drawLayer -= 1;
            } else if (event.KeyInput.Key == KEY_PERIOD && event.KeyInput.PressedDown) {
                if (drawLayer < numLayers - 1)
                    drawLayer += 1;
            }
            // std::cout << "key " << event.KeyInput.Key;
            // if (event.KeyInput.PressedDown)
            //     std::cout << " down";
            // else
            //     std::cout << " up";
            // std::cout << std::endl;
        } else if (event.EventType == irr::EET_MOUSE_INPUT_EVENT)
        {
            switch(event.MouseInput.Event)
            {
            case EMIE_LMOUSE_PRESSED_DOWN:
                MouseState.LeftButtonDown = true;
                if (highlight->isVisible())
                    selectCell(highlight->getID());
                break;

            case EMIE_LMOUSE_LEFT_UP:
                MouseState.LeftButtonDown = false;
                break;

            case EMIE_MOUSE_MOVED:
                MouseState.Position.X = event.MouseInput.X;
                MouseState.Position.Y = event.MouseInput.Y;
                break;

            default:
                // We won't use the wheel
                break;
            }
        }
        return false;
    }

    // returns whether a key is being held down
    virtual bool IsKeyDown(EKEY_CODE keyCode) const
    {
        return KeyIsDown[keyCode];
    }

    const SMouseState & GetMouseState(void) const
    {
        return MouseState;
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

MyEventReceiver receiver;

const video::SColor cellColours[] = {
    video::SColor(255, 255, 255, 255),  // white
    video::SColor(255, 255, 48, 48),    // red
    video::SColor(255, 255, 150, 48),   // orange
    video::SColor(255, 255, 248, 48),   // yellow
    video::SColor(255, 54, 255, 48),    // green
    video::SColor(255, 48, 200, 255),   // cyan
    video::SColor(255, 88, 48, 255),    // blue
    video::SColor(255, 168, 48, 255),   // purple
    video::SColor(255, 255, 48, 237)    // pink
};

void PrintInstructions(){
    // print the keyboard controls to console

    std::cout << "\nWelcome to 3DLife!\n\n";

    std::cout << "Controls\n" 
        << "----------------------------------\n" 
        << "Orbit Left             " << "Left arrow" << "\n" 
        << "Orbit Up               " << "Up arrow" << "\n" 
        << "Orbit Right            " << "Right arrow" << "\n" 
        << "Orbit Down             " << "Down arrow" << "\n" 
        << "Zoom Out               " << "Plus key" << "\n" 
        << "Zoom In                " << "Minus key" << "\n" 
        << "Reset Camera           " << "Right Shift" << "\n" 
        << "Draw Cells             " << "D" << "\n" 
        << "Increment Draw Layer   " << "Period" << "\n" 
        << "Decrement Draw Layer   " << "Comma" << "\n" 
        << std::endl;
}

int startShmem() {

    //Open the file mapping and map it as read-only
    m_file = boost::interprocess::file_mapping("/tmp/3DLifeShmem", boost::interprocess::read_only);

    region = boost::interprocess::mapped_region(m_file, boost::interprocess::read_only);

    data = reinterpret_cast<TransferData*>(region.get_address());
    // std::cout << "C++ Program - Getting Data" << std::endl;
    
    numDimensions = 0;
    int maxDimensions = sizeof(data->dimensions) / 4;
    // std::cout << "Num Dims " << maxDimensions << "\n";
    for (int i = 0; i < maxDimensions; i++) {
        if (data->dimensions[i] == 0)
            break;
        numDimensions += 1;
    }

    // std::cout << "\n";

    // std::cout << "Drawmode " << (data->drawMode) << "\n";

}

void startIrrlicht() {
    /*******************
     * Set up Irrlicht *
     *******************/

    // ask user to select driver
    video::E_DRIVER_TYPE driverType = driverChoiceConsole();

    // start up the engine
    device = createDevice(driverType, core::dimension2d<u32>(640,480));
    if (device == 0)
        throw std::runtime_error( "could not create the selected driver" );

    // Make event receiver handle inputs
    device->setEventReceiver(&receiver);

    driver = device->getVideoDriver();
    smgr = device->getSceneManager();
    meshman = smgr->getMeshManipulator();
}

void setCubeColor(scene::IMeshSceneNode* cube, video::SColor color) {
    meshman->setVertexColors(cube->getMesh(), color); 
    // could also use
    // cells[i]->getMaterial(0).AmbientColor = video::SColor(255, 0, 0, 255);
}

void initializeSimulation() {

    scene::ITriangleSelector* selector = 0;

    unsigned long cellsPerDimension[numDimensions];
    cellsPerDimension[0] = data->dimensions[0];
    // std::cout << "CPD[0] = " << cellsPerDimension[0] << "\n";
    for (unsigned int i=1; i < numDimensions; i++) {
        cellsPerDimension[i] = data->dimensions[i] * cellsPerDimension[i-1];
        // std::cout << "CPD[" << i << "] = " << cellsPerDimension[i] << "\n";
    }

    unsigned long linCellsPerDimension[numDimensions];
    for (int i=0; i < (int)numDimensions; i++) {
        if (i - 3 >= 0) {
            linCellsPerDimension[i] = data->dimensions[i] * linCellsPerDimension[i - 3];
        } else {
            linCellsPerDimension[i] = data->dimensions[i];
        }
        // std::cout << "CPD[" << i << "] = " << linCellsPerDimension[i] << "\n";
    }

    numLayers = 1;
    for (unsigned int i = 2; i < numDimensions; i += 3) {
        numLayers *= data->dimensions[i];
    }

    unsigned int dimensionSizes[numDimensions];
    unsigned int padding;
    for (unsigned int i=0; i < numDimensions; i++) {
        if (i < 3) {
            dimensionSizes[i] = data->dimensions[i] * cellSize;
        } else {
            padding = std::pow(cellSize*2, i/3);
            dimensionSizes[i] = (dimensionSizes[i-3] + padding) * data->dimensions[i] - padding;
        }
    }

    // get the initial state of the simulation
    numCells = cellsPerDimension[numDimensions - 1];
    std::cout << "Simulating " << numCells << " cells...\n";

    // we need a cube node for each cell
    cells.resize(numCells);

    // store each cell's x, y and z grid coordinates
    gridPositions.resize(numCells * 3);
    
    for(unsigned int c = 0; c < numCells; c++) {
        // calculate the position of this cell in an n-dimensional grid
        
        // intialize x = y = z = 0;
        unsigned int pos[3] = {0}; 
        unsigned int gridPos[3] = {0}; 

        pos[0] += c % data->dimensions[0] * cellSize;
        gridPos[0] += c % data->dimensions[0];

        for(unsigned int d=1; d < numDimensions; d++) {
            if (d < 3) {
                pos[d] += c / cellsPerDimension[d-1] % data->dimensions[d] * cellSize; 
                gridPos[d] += c / cellsPerDimension[d-1] % data->dimensions[d];
            } else {
                padding = std::pow(cellSize*2, d/3);
                pos[d % 3] += (dimensionSizes[d - 3] + padding) * (c / cellsPerDimension[d-1] % data->dimensions[d]);
                
                gridPos[d % 3] += (c / cellsPerDimension[d-1] % data->dimensions[d]) * linCellsPerDimension[d-3];
            }
        }

        gridPositions[c * 3] = gridPos[0];
        gridPositions[c * 3 + 1] = gridPos[1];
        gridPositions[c * 3 + 2] = gridPos[2];

        // create a cube node to represent this cell
        cells[c] = smgr->addCubeSceneNode(
            cellSize,                                   // size
            0,                                          // parent node
            c,                                         // id
            core::vector3df(pos[0], pos[1], pos[2]),    // position
            core::vector3df(0,0,0),                     // rotation
            core::vector3df(1.0f,1.0f,1.0f)             // scale
        );
        // could also use cells[i]->setPosition();    

        // set up collision detection for this cell
        selector = smgr->createTriangleSelector(cells[c]->getMesh(), cells[c]); 
        cells[c]->setTriangleSelector(selector);
        selector->drop();   
        
        // disable lighting for the cube
        cells[c]->setMaterialFlag(video::EMF_LIGHTING, false);
    }

    // add a cube that will highlight selected cells
    highlight = smgr->addCubeSceneNode(
            cellSize, 0, -1,                      
            core::vector3df(-1000, 0, 0),
            core::vector3df(0, 0, 0),  
            core::vector3df(highlightScale, highlightScale, highlightScale)
        );
    setCubeColor(highlight, highlightColor);
    // make it transparent and disable lighting
    highlight->setMaterialType(video::EMT_TRANSPARENT_ADD_COLOR); 
    highlight->setMaterialFlag(video::EMF_LIGHTING, false);
    // highlight->setMaterialFlag(video::EMF_ZBUFFER, false);

    // add an empty for the camera to pivot around
    cameraPivot = smgr->addEmptySceneNode();
    core::vector3df sceneCenter(
        ((numDimensions-1) / 3 * 3) / 2,
        ((numDimensions-2) / 3 * 3 + 1) / 2,
        ((numDimensions-3) / 3 * 3 + 2) / 2
    );
    cameraPivot->setPosition(sceneCenter);

    // add camera
    cam = smgr->addCameraSceneNode(cameraPivot);
    cam->setTarget( cameraPivot->getAbsolutePosition() );
}

void updateCamera(f32 deltaTime) {
    // adjust camera position based on current key input
    if (receiver.IsKeyDown(KEY_PLUS))
        camRadius -= (camLinearVelocity * deltaTime);
    if (receiver.IsKeyDown(KEY_MINUS))
        camRadius += (camLinearVelocity * deltaTime);
    if (receiver.IsKeyDown(KEY_LEFT))
        camTheta += (camAngularVelocity * deltaTime);
    if (receiver.IsKeyDown(KEY_RIGHT))
        camTheta -= (camAngularVelocity * deltaTime);
    if (receiver.IsKeyDown(KEY_DOWN))
        camPhi += (camAngularVelocity * deltaTime);
    if (receiver.IsKeyDown(KEY_UP))
        camPhi -= (camAngularVelocity * deltaTime);
    if (receiver.IsKeyDown(KEY_RSHIFT))
    {
        // reset rotation and zoom
        camTheta  = 180.f;
        camPhi    = 90.f;
        camRadius = 20.f;
    }

    // restrict maximum zoom
    if (camRadius < 1.f)
        camRadius = 1.f;

    // lame ass gimble lock prevention. if you don't want to do this
    // you need to adjust the up vector of the camera so it never is
    // parallel to the look at vector
    if (camPhi < 10.f)
        camPhi = 10.f;
    else if (170.f < camPhi)
        camPhi = 170.f;

    f32 sinOfPhi = sinf(camPhi * core::DEGTORAD);
    f32 cosOfPhi = cosf(camPhi * core::DEGTORAD);

    f32 sinOfTheta = sinf(camTheta * core::DEGTORAD);
    f32 cosOfTheta = cosf(camTheta * core::DEGTORAD);

    core::vector3df offset;

    offset.X = camRadius * sinOfTheta * sinOfPhi;
    offset.Y = camRadius * cosOfPhi;
    offset.Z = camRadius * cosOfTheta * sinOfPhi;

    // camera is a child of the cube, so our offset is 
    // actually the position of the camera
    cam->setPosition(offset);
    cam->setTarget( cameraPivot->getAbsolutePosition() );
    cam->updateAbsolutePosition();
}

void updateSimulation() {
    for(unsigned int c = 0; c < numCells; c++) {

        // get this cell's state
        if (data->cells[c] > sizeof(cellColours)/sizeof(*cellColours)) {
            std::cerr << "No colour defined for cell state " << data->cells[c];
            data->cells[c] = data->cells[c] % sizeof(cellColours)/sizeof(*cellColours);
            std::cerr << ". Using cell state " << data->cells[c] << " instead\n";
        }

        if (drawMode) {
            if (gridPositions[c * 3 + 2] != drawLayer)
                cells[c]->setVisible(false);
            else {
                cells[c]->setVisible(true);
                if (data->cells[c] == 0) {
                    // color invisible cells black in draw mode
                    setCubeColor(cells[c], video::SColor(0, 0, 0, 0));
                } else {
                    // colour cell based on its state
                    setCubeColor(cells[c], cellColours[data->cells[c]-1]);
                }
            }
        } else {
            if (data->cells[c] == 0) {
                cells[c]->setVisible(false);
            } else {
                cells[c]->setVisible(true);
                // colour cell based on its state
                setCubeColor(cells[c], cellColours[data->cells[c]-1]);
            }
        }
        // greyscale
        // smgr->getMeshManipulator()->setVertexColors(cells[c]->getMesh(), 
        //     video::SColor(255, c*10%255, c*10%255, c*10%255)
        // );
    }
}

void EndIrrlicht() {
    // drop the graphics device
    device->drop();
}

int main(int argc, char *argv[]){

    startShmem();    

    startIrrlicht();

    initializeSimulation();

    PrintInstructions();

    while(device->run())
    {
        // calculate deltaTime time as fractional seconds
        now = device->getTimer()->getRealTime();
        deltaTime = (now - lastFrameTime) / 1000.f;
        lastFrameTime = now;
        
        updateSimulation();

        if(drawMode) {
            core::line3df ray = smgr->getSceneCollisionManager()->getRayFromScreenCoordinates(receiver.GetMouseState().Position, cam);

            // Stores closest intersection point with mouse ray and cells
            core::vector3df intersection;

            // Used to show with triangle has been hit
            core::triangle3df hitTriangle;

            // This call is all you need to perform ray/triangle collision on every scene node
            // that has a triangle selector, (all cells).  It finds the nearest
            // collision point/triangle, and returns the scene node containing that point.
            scene::ISceneNode * selectedSceneNode =
                smgr->getSceneCollisionManager()
                    ->getSceneNodeAndCollisionPointFromRay(
                        ray,
                        intersection, // The position of the collision
                        hitTriangle   // The triangle hit in the collision
                ); 

            // If the ray hit anything, move the billboard to the collision position
            // and draw the triangle that was hit.

            if(selectedSceneNode)
            {
                if (highlight->getAbsolutePosition() != selectedSceneNode->getAbsolutePosition()) {
                    if (receiver.MouseState.LeftButtonDown)
                        selectCell(selectedSceneNode->getID());

                    highlight->setID(selectedSceneNode->getID());
                    highlight->setPosition(selectedSceneNode->getAbsolutePosition());
                    highlight->setVisible(true);
                }
            }
        } else {
            highlight->setID(-1);
            highlight->setVisible(false);
        }

        // window is active, so render scene
        if (device->isWindowActive())
        {
            if (driver->beginScene(true, true, video::SColor(255, 100, 100, 140)))
            {
                smgr->drawAll();

                driver->endScene();
            }

            // only update the camera if window is receiving inputs
            updateCamera(deltaTime);
        }
    }
    
    EndIrrlicht();

    return 0;
}