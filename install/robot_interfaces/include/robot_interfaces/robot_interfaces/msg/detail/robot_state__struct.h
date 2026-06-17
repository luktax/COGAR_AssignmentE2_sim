// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robot_interfaces:msg/RobotState.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__ROBOT_STATE__STRUCT_H_
#define ROBOT_INTERFACES__MSG__DETAIL__ROBOT_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in msg/RobotState in the package robot_interfaces.
typedef struct robot_interfaces__msg__RobotState
{
  std_msgs__msg__Header header;
  double q[19];
  double dq[18];
  double imu_quat[4];
  double imu_gyro[3];
  double time;
} robot_interfaces__msg__RobotState;

// Struct for a sequence of robot_interfaces__msg__RobotState.
typedef struct robot_interfaces__msg__RobotState__Sequence
{
  robot_interfaces__msg__RobotState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robot_interfaces__msg__RobotState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOT_INTERFACES__MSG__DETAIL__ROBOT_STATE__STRUCT_H_
