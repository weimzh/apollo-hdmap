/******************************************************************************
 * Copyright 2018 The Apollo Authors. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *****************************************************************************/

#include "py_map.h"
#include "log.h"

#include <limits>
#include <set>
#include <string>

#include <Python.h>

using apollo::hdmap::PyHdMap;

#define PYOBJECT_NULL_STRING PyBytes_FromStringAndSize("", 0)
#define C_STR_TO_PY_BYTES(cstr) \
  PyBytes_FromStringAndSize(cstr.c_str(), cstr.size())

template <typename T>
T PyObjectToPtr(PyObject *pyobj, const std::string &type_ptr) {
  T obj_ptr = (T)PyCapsule_GetPointer(pyobj, type_ptr.c_str());
  if (obj_ptr == nullptr) {
    AERROR << "PyObjectToPtr failed,type->" << type_ptr << "pyobj: " << pyobj;
  }
  return obj_ptr;
}

PyObject *apollo_new_PyHdMap(PyObject *self, PyObject *args) {
  PyHdMap *hdmap = new PyHdMap();
  return PyCapsule_New(hdmap, "apollo_hdmap_pyhdmap", nullptr);
}

PyObject *apollo_delete_PyHdMap(PyObject *self, PyObject *args) {
  PyObject *pyobj_hdmap = nullptr;
  if (!PyArg_ParseTuple(args, const_cast<char *>("O:delete_PyHdMap"),
                        &pyobj_hdmap)) {
    Py_INCREF(Py_None);
    return Py_None;
  }

  auto *hdmap = reinterpret_cast<PyHdMap *>(PyCapsule_GetPointer(
      pyobj_hdmap, "apollo_hdmap_pyhdmap"));
  if (nullptr == hdmap) {
    AERROR << "delete_PyHdMap:hdmap ptr is null!";
    Py_INCREF(Py_None);
    return Py_None;
  }
  delete hdmap;
  Py_INCREF(Py_None);
  return Py_None;
}

PyObject *apollo_PyHdMap_LoadMapFromFile(PyObject *self, PyObject *args) {
  PyObject *pyobj_hdmap = nullptr;
  char *map_filename = nullptr;
  if (!PyArg_ParseTuple(args,
                        const_cast<char *>("Os:PyHdMap_LoadMapFromFile"),
                        &pyobj_hdmap, &map_filename)) {
    AERROR << "PyHdMap_LoadMapFromFile failed!";
    return PYOBJECT_NULL_STRING;
  }

  auto *hdmap = reinterpret_cast<PyHdMap *>(PyCapsule_GetPointer(
      pyobj_hdmap, "apollo_hdmap_pyhdmap"));
  if (nullptr == hdmap) {
    AERROR << "PyHdMap_LoadMapFromFile ptr is null!";
    return PYOBJECT_NULL_STRING;
  }

  int ret = hdmap->LoadMapFromFile(map_filename);
  return PyLong_FromUnsignedLongLong(ret);
}


static PyMethodDef _apollo_hdmap_methods[] = {
    // PyHdMap fun
    {"new_PyHdMap", apollo_new_PyHdMap, METH_VARARGS, ""},
    {"delete_PyHdMap", apollo_delete_PyHdMap, METH_VARARGS, ""},
    {"PyHdMap_LoadMapFromFile", apollo_PyHdMap_LoadMapFromFile, METH_VARARGS, ""},
    {nullptr, nullptr, 0, nullptr} /* sentinel */
};

/// Init function of this module
PyMODINIT_FUNC PyInit__apollo_hdmap_wrapper(void) {
  static struct PyModuleDef module_def = {
      PyModuleDef_HEAD_INIT,
      "_apollo_hdmap_wrapper",  // Module name.
      "Apollo HDMap module",    // Module doc.
      -1,                       // Module size.
      _apollo_hdmap_methods,    // Module methods.
      nullptr,
      nullptr,
      nullptr,
      nullptr,
  };

  AINFO << "init _apollo_hdmap_wrapper";
  return PyModule_Create(&module_def);
}
