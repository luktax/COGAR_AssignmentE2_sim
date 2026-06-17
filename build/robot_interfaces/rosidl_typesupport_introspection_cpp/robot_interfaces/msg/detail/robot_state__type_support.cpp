// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from robot_interfaces:msg/RobotState.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "robot_interfaces/msg/detail/robot_state__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace robot_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void RobotState_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) robot_interfaces::msg::RobotState(_init);
}

void RobotState_fini_function(void * message_memory)
{
  auto typed_message = static_cast<robot_interfaces::msg::RobotState *>(message_memory);
  typed_message->~RobotState();
}

size_t size_function__RobotState__q(const void * untyped_member)
{
  (void)untyped_member;
  return 19;
}

const void * get_const_function__RobotState__q(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 19> *>(untyped_member);
  return &member[index];
}

void * get_function__RobotState__q(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 19> *>(untyped_member);
  return &member[index];
}

void fetch_function__RobotState__q(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__RobotState__q(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__RobotState__q(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__RobotState__q(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

size_t size_function__RobotState__dq(const void * untyped_member)
{
  (void)untyped_member;
  return 18;
}

const void * get_const_function__RobotState__dq(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 18> *>(untyped_member);
  return &member[index];
}

void * get_function__RobotState__dq(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 18> *>(untyped_member);
  return &member[index];
}

void fetch_function__RobotState__dq(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__RobotState__dq(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__RobotState__dq(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__RobotState__dq(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

size_t size_function__RobotState__imu_quat(const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * get_const_function__RobotState__imu_quat(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 4> *>(untyped_member);
  return &member[index];
}

void * get_function__RobotState__imu_quat(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 4> *>(untyped_member);
  return &member[index];
}

void fetch_function__RobotState__imu_quat(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__RobotState__imu_quat(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__RobotState__imu_quat(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__RobotState__imu_quat(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

size_t size_function__RobotState__imu_gyro(const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * get_const_function__RobotState__imu_gyro(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void * get_function__RobotState__imu_gyro(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void fetch_function__RobotState__imu_gyro(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__RobotState__imu_gyro(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__RobotState__imu_gyro(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__RobotState__imu_gyro(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember RobotState_message_member_array[6] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robot_interfaces::msg::RobotState, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "q",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    19,  // array size
    false,  // is upper bound
    offsetof(robot_interfaces::msg::RobotState, q),  // bytes offset in struct
    nullptr,  // default value
    size_function__RobotState__q,  // size() function pointer
    get_const_function__RobotState__q,  // get_const(index) function pointer
    get_function__RobotState__q,  // get(index) function pointer
    fetch_function__RobotState__q,  // fetch(index, &value) function pointer
    assign_function__RobotState__q,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "dq",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    18,  // array size
    false,  // is upper bound
    offsetof(robot_interfaces::msg::RobotState, dq),  // bytes offset in struct
    nullptr,  // default value
    size_function__RobotState__dq,  // size() function pointer
    get_const_function__RobotState__dq,  // get_const(index) function pointer
    get_function__RobotState__dq,  // get(index) function pointer
    fetch_function__RobotState__dq,  // fetch(index, &value) function pointer
    assign_function__RobotState__dq,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "imu_quat",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    4,  // array size
    false,  // is upper bound
    offsetof(robot_interfaces::msg::RobotState, imu_quat),  // bytes offset in struct
    nullptr,  // default value
    size_function__RobotState__imu_quat,  // size() function pointer
    get_const_function__RobotState__imu_quat,  // get_const(index) function pointer
    get_function__RobotState__imu_quat,  // get(index) function pointer
    fetch_function__RobotState__imu_quat,  // fetch(index, &value) function pointer
    assign_function__RobotState__imu_quat,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "imu_gyro",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(robot_interfaces::msg::RobotState, imu_gyro),  // bytes offset in struct
    nullptr,  // default value
    size_function__RobotState__imu_gyro,  // size() function pointer
    get_const_function__RobotState__imu_gyro,  // get_const(index) function pointer
    get_function__RobotState__imu_gyro,  // get(index) function pointer
    fetch_function__RobotState__imu_gyro,  // fetch(index, &value) function pointer
    assign_function__RobotState__imu_gyro,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "time",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robot_interfaces::msg::RobotState, time),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers RobotState_message_members = {
  "robot_interfaces::msg",  // message namespace
  "RobotState",  // message name
  6,  // number of fields
  sizeof(robot_interfaces::msg::RobotState),
  RobotState_message_member_array,  // message members
  RobotState_init_function,  // function to initialize message memory (memory has to be allocated)
  RobotState_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t RobotState_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &RobotState_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace robot_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<robot_interfaces::msg::RobotState>()
{
  return &::robot_interfaces::msg::rosidl_typesupport_introspection_cpp::RobotState_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, robot_interfaces, msg, RobotState)() {
  return &::robot_interfaces::msg::rosidl_typesupport_introspection_cpp::RobotState_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
