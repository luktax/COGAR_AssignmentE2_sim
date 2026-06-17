// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:msg/RobotState.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__ROBOT_STATE__BUILDER_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__ROBOT_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/msg/detail/robot_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace msg
{

namespace builder
{

class Init_RobotState_time
{
public:
  explicit Init_RobotState_time(::robot_interfaces::msg::RobotState & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::msg::RobotState time(::robot_interfaces::msg::RobotState::_time_type arg)
  {
    msg_.time = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::msg::RobotState msg_;
};

class Init_RobotState_imu_gyro
{
public:
  explicit Init_RobotState_imu_gyro(::robot_interfaces::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_time imu_gyro(::robot_interfaces::msg::RobotState::_imu_gyro_type arg)
  {
    msg_.imu_gyro = std::move(arg);
    return Init_RobotState_time(msg_);
  }

private:
  ::robot_interfaces::msg::RobotState msg_;
};

class Init_RobotState_imu_quat
{
public:
  explicit Init_RobotState_imu_quat(::robot_interfaces::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_imu_gyro imu_quat(::robot_interfaces::msg::RobotState::_imu_quat_type arg)
  {
    msg_.imu_quat = std::move(arg);
    return Init_RobotState_imu_gyro(msg_);
  }

private:
  ::robot_interfaces::msg::RobotState msg_;
};

class Init_RobotState_dq
{
public:
  explicit Init_RobotState_dq(::robot_interfaces::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_imu_quat dq(::robot_interfaces::msg::RobotState::_dq_type arg)
  {
    msg_.dq = std::move(arg);
    return Init_RobotState_imu_quat(msg_);
  }

private:
  ::robot_interfaces::msg::RobotState msg_;
};

class Init_RobotState_q
{
public:
  explicit Init_RobotState_q(::robot_interfaces::msg::RobotState & msg)
  : msg_(msg)
  {}
  Init_RobotState_dq q(::robot_interfaces::msg::RobotState::_q_type arg)
  {
    msg_.q = std::move(arg);
    return Init_RobotState_dq(msg_);
  }

private:
  ::robot_interfaces::msg::RobotState msg_;
};

class Init_RobotState_header
{
public:
  Init_RobotState_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotState_q header(::robot_interfaces::msg::RobotState::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_RobotState_q(msg_);
  }

private:
  ::robot_interfaces::msg::RobotState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::msg::RobotState>()
{
  return robot_interfaces::msg::builder::Init_RobotState_header();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__ROBOT_STATE__BUILDER_HPP_
