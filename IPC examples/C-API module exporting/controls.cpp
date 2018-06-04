#include "Main.cpp"

// define the methods implemented by this module

// sets draw mode true / false
static PyObject * set_draw_mode(PyObject *self, PyObject *args)
{
    const bool *state;

    // parse argument as boolean, handles errors (trust me)
    if (!PyArg_ParseTuple(args, "p", &state)) 
        return NULL;

    std::cout << "Setting state to " << &state << "\n";
    drawMode = &state;

    // return none
    Py_INCREF(Py_None);
    return Py_None;
}

// create a method table for our module
static PyMethodDef ControlsMethods[] = {
    {"set_draw_mode",  set_draw_mode, METH_VARARGS,
     "Set draw mode to true or false."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

// set up module definition structure
static struct PyModuleDef controlsmodule = {
    PyModuleDef_HEAD_INIT,
    "controls",   /* name of module */
    "Python module providing interface to C++ code", /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    ControlsMethods
};

// create module initialization function
PyMODINIT_FUNC PyInit_controls(void)
{
    return PyModule_Create(&controlsmodule);
}

// static PyObject * set_draw_mode(PyObject *self, PyObject *args)
// {
//     const char *command;
//     int sts;

//     if (!PyArg_ParseTuple(args, "s", &command))
//         return NULL;
//     sts = system(command);
//     return Py_BuildValue("i", sts);
// }

