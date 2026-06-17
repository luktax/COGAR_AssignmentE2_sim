// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robot_interfaces:srv/UpdateGaitParams.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__SRV__DETAIL__UPDATE_GAIT_PARAMS__STRUCT_H_
#define ROBOT_INTERFACES__SRV__DETAIL__UPDATE_GAIT_PARAMS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'phase_offset'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in srv/UpdateGaitParams in the package robot_interfaces.
typedef struct robot_interfaces__srv__UpdateGaitParams_Request
{
  float frequency_hz;
  float duty_cycle;
  float height_swing;
  rosidl_runtime_c__float__Sequence phase_offset;
} robot_interfaces__srv__UpdateGaitParams_Request;

// Struct for a sequence of robot_interfaces__srv__UpdateGaitParams_Request.
typedef struct robot_interfaces__srv__UpdateGaitParams_Request__Sequence
{
  robot_interfaces__srv__UpdateGaitParams_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_interfaces__srv__UpdateGaitParams_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/UpdateGaitParams in the package robot_interfaces.
typedef struct robot_interfaces__srv__UpdateGaitParams_Response
{
  bool success;
  rosidl_runtime_c__String message;
} robot_interfaces__srv__UpdateGaitParams_Response;

// Struct for a sequence of robot_interfaces__srv__UpdateGaitParams_Response.
typedef struct robot_interfaces__srv__UpdateGaitParams_Response__Sequence
{
  robot_interfaces__srv__UpdateGaitParams_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_interfaces__srv__UpdateGaitParams_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_INTERFACES__SRV__DETAIL__UPDATE_GAIT_PARAMS__STRUCT_H_
