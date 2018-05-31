#include <Python.h>

PyObject *pName, *pModule, *pDict, *pFunc, *pValue, *pArgs, *pClass, *pInstance;

int EndPython(){
    Py_XDECREF(pInstance); //using XDECREF instead of DECREF to avoid problems is pInstance is NULL
    Py_XDECREF(pValue);
    Py_XDECREF(pModule);
    Py_XDECREF(pName);
    Py_Finalize();
    return 1;
}

int main(int argc, char *argv[]){


    Py_Initialize();//Initialize the Python interpreter

    PyRun_SimpleString("import sys\n");
    PyRun_SimpleString("sys.path.append(\"/home/kikai/Documents/FIT2083/3DLife/c-python\")");//the folder where the pythonTest.py is located


    pName = PyUnicode_FromString("pythonTest");//creates new reference so you have to DECREF if

    pModule = PyImport_Import(pName);//import module pythonTest.py. New reference
    if(pModule==NULL)return EndPython(); //no module found or there was an error when compiling python code

    pDict = PyModule_GetDict(pModule);//borowed reference so no DECREF

    ///function call and return test
    pFunc = PyDict_GetItemString(pDict, "getLong");//borowed reference. choose file is the name of the funcion
    if(pFunc==NULL) {
        printf("No such function getLong\n");
        return EndPython();
    } //no such function
    pValue =PyObject_CallObject(pFunc, NULL);//arguments are null pValue is the return of test1 function
    printf("Return of call 1: %ld\n",PyLong_AsLong(pValue));
    ///----------------------

    ///function call and return list test
    pFunc = PyDict_GetItemString(pDict, "get_state");//borowed reference
    if(pFunc==NULL) {
        printf("No such function get_state\n");
        return EndPython();
    } //no such function
    pValue =PyObject_CallObject(pFunc, NULL);//arguments are null pValue is the return of test1 function
    printf("Size of the c++ list is: %ld\n", PyList_Size(pValue));
    ///----------------------

    ///function call with paramater and return test
    pArgs = PyTuple_New(1);// save arguments in a PyTuple
    pValue = PyLong_FromLong(7);
    PyTuple_SetItem(pArgs, 0, pValue);

    pFunc = PyDict_GetItemString(pDict, "test2");
    if(pFunc==NULL)return EndPython();
    pValue =PyObject_CallObject(pFunc, pArgs);
    printf("Return of call 2: %ld\n",PyLong_AsLong(pValue));
    ///--------------------

    ///function call with multiple paramaters and return test
    pArgs = PyTuple_New(2);
    for (int i = 0; i < 2; i++) {
        pValue = PyLong_FromLong(i+4);
        PyTuple_SetItem(pArgs, i, pValue);
    }
    pFunc = PyDict_GetItemString(pDict, "test3");
    if(pFunc==NULL)return EndPython();
    pValue=PyObject_CallObject(pFunc, pArgs);
    printf("Result of call 3: %ld\n", PyLong_AsLong(pValue));
    ///-------------------------------------------------

     ///wxPython gui test
    pFunc = PyDict_GetItemString(pDict, "chooseFile");
    if(pFunc==NULL)return EndPython();
    pValue =PyObject_CallObject(pFunc, NULL);
    printf("Return of call 4: %s\n",PyBytes_AsString(pValue));
    ///-----------------

    ///calling a python obyect test
    pClass = PyDict_GetItemString(pDict, "testClass");//geting the class. boroved reference
    if (PyCallable_Check(pClass)) {//no such class or class not callable
        pInstance = PyObject_CallObject(pClass, NULL);//geting an instance. new reference. Arguents for the constructor are NULL
    }else{
        return EndPython();
    }
    pValue = PyObject_CallMethod(pInstance, "setAB", "(ii)", 12, 11); //call method setAB with argiments int int "(ii)" 12,11
    pValue = PyObject_CallMethod(pInstance, "multiply", NULL);
    printf("Return of call 5: %ld\n", PyLong_AsLong(pValue));
    ///------------------------------------

    EndPython();


    return 0;
}