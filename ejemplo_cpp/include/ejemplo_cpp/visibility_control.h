#ifndef EJEMPLO_CPP__VISIBILITY_CONTROL_H_
#define EJEMPLO_CPP__VISIBILITY_CONTROL_H_

#ifdef __cplusplus
extern "C"
{
#endif

// This logic was borrowed (then namespaced) from the examples on the gcc wiki:
//     https://gcc.gnu.org/wiki/Visibility

#if defined _WIN32 || defined __CYGWIN__
  #ifdef __GNUC__
    #define EJEMPLO_CPP_EXPORT __attribute__ ((dllexport))
    #define EJEMPLO_CPP_IMPORT __attribute__ ((dllimport))
  #else
    #define EJEMPLO_CPP_EXPORT __declspec(dllexport)
    #define EJEMPLO_CPP_IMPORT __declspec(dllimport)
  #endif
  #ifdef EJEMPLO_CPP_BUILDING_DLL
    #define EJEMPLO_CPP_PUBLIC EJEMPLO_CPP_EXPORT
  #else
    #define EJEMPLO_CPP_PUBLIC EJEMPLO_CPP_IMPORT
  #endif
  #define EJEMPLO_CPP_PUBLIC_TYPE EJEMPLO_CPP_PUBLIC
  #define EJEMPLO_CPP_LOCAL
#else
  #define EJEMPLO_CPP_EXPORT __attribute__ ((visibility("default")))
  #define EJEMPLO_CPP_IMPORT
  #if __GNUC__ >= 4
    #define EJEMPLO_CPP_PUBLIC __attribute__ ((visibility("default")))
    #define EJEMPLO_CPP_LOCAL  __attribute__ ((visibility("hidden")))
  #else
    #define EJEMPLO_CPP_PUBLIC
    #define EJEMPLO_CPP_LOCAL
  #endif
  #define EJEMPLO_CPP_PUBLIC_TYPE
#endif

#ifdef __cplusplus
}
#endif

#endif  // EJEMPLO_CPP__VISIBILITY_CONTROL_H_