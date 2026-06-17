// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robot_interfaces:srv/SetBodyHeight.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__SRV__DETAIL__SET_BODY_HEIGHT__STRUCT_H_
#define ROBOT_INTERFACES__SRV__DETAIL__SET_BODY_HEIGHT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/SetBodyHeight in the package robot_interfaces.
typedef struct robot_interfaces__srv__SetBodyHeight_Request
{
  float height;
} robot_interfaces__srv__SetBodyHeight_Request;

// Struct for a sequence of robot_interfaces__srv__SetBodyHeight_Request.
typedef struct robot_interfaces__srv__SetBodyHeight_Request__Sequence
{
  robot_interfaces__srv__SetBodyHeight_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_interfaces__srv__SetBodyHeight_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SetBodyHeight in the package robot_interfaces.
typedef struct robot_interfaces__srv__SetBodyHeight_Response
{
  bool success;
  rosidl_runtime_c__String message;
} robot_interfaces__srv__SetBodyHeight_Response;

// Struct for a sequence of robot_interfaces__srv__SetBodyHeight_Response.
typedef struct robot_interfaces__srv__SetBodyHeight_Response__Sequence
{
  robot_interfaces__srv__SetBodyHeight_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_interfaces__srv__SetBodyHeight_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_INTERFACES__SRV__DETAIL__SET_BODY_HEIGHT__STRUCT_H_
