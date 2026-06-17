// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:srv/UpdateGaitParams.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__SRV__DETAIL__UPDATE_GAIT_PARAMS__BUILDER_HPP_
#define ROBOT_INTERFACES__SRV__DETAIL__UPDATE_GAIT_PARAMS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/srv/detail/update_gait_params__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace srv
{

namespace builder
{

class Init_UpdateGaitParams_Request_phase_offset
{
public:
  explicit Init_UpdateGaitParams_Request_phase_offset(::robot_interfaces::srv::UpdateGaitParams_Request & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::srv::UpdateGaitParams_Request phase_offset(::robot_interfaces::srv::UpdateGaitParams_Request::_phase_offset_type arg)
  {
    msg_.phase_offset = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::srv::UpdateGaitParams_Request msg_;
};

class Init_UpdateGaitParams_Request_height_swing
{
public:
  explicit Init_UpdateGaitParams_Request_height_swing(::robot_interfaces::srv::UpdateGaitParams_Request & msg)
  : msg_(msg)
  {}
  Init_UpdateGaitParams_Request_phase_offset height_swing(::robot_interfaces::srv::UpdateGaitParams_Request::_height_swing_type arg)
  {
    msg_.height_swing = std::move(arg);
    return Init_UpdateGaitParams_Request_phase_offset(msg_);
  }

private:
  ::robot_interfaces::srv::UpdateGaitParams_Request msg_;
};

class Init_UpdateGaitParams_Request_duty_cycle
{
public:
  explicit Init_UpdateGaitParams_Request_duty_cycle(::robot_interfaces::srv::UpdateGaitParams_Request & msg)
  : msg_(msg)
  {}
  Init_UpdateGaitParams_Request_height_swing duty_cycle(::robot_interfaces::srv::UpdateGaitParams_Request::_duty_cycle_type arg)
  {
    msg_.duty_cycle = std::move(arg);
    return Init_UpdateGaitParams_Request_height_swing(msg_);
  }

private:
  ::robot_interfaces::srv::UpdateGaitParams_Request msg_;
};

class Init_UpdateGaitParams_Request_frequency_hz
{
public:
  Init_UpdateGaitParams_Request_frequency_hz()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_UpdateGaitParams_Request_duty_cycle frequency_hz(::robot_interfaces::srv::UpdateGaitParams_Request::_frequency_hz_type arg)
  {
    msg_.frequency_hz = std::move(arg);
    return Init_UpdateGaitParams_Request_duty_cycle(msg_);
  }

private:
  ::robot_interfaces::srv::UpdateGaitParams_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::srv::UpdateGaitParams_Request>()
{
  return robot_interfaces::srv::builder::Init_UpdateGaitParams_Request_frequency_hz();
}

}  // namespace robot_interfaces


namespace robot_interfaces
{

namespace srv
{

namespace builder
{

class Init_UpdateGaitParams_Response_message
{
public:
  explicit Init_UpdateGaitParams_Response_message(::robot_interfaces::srv::UpdateGaitParams_Response & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::srv::UpdateGaitParams_Response message(::robot_interfaces::srv::UpdateGaitParams_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::srv::UpdateGaitParams_Response msg_;
};

class Init_UpdateGaitParams_Response_success
{
public:
  Init_UpdateGaitParams_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_UpdateGaitParams_Response_message success(::robot_interfaces::srv::UpdateGaitParams_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_UpdateGaitParams_Response_message(msg_);
  }

private:
  ::robot_interfaces::srv::UpdateGaitParams_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::srv::UpdateGaitParams_Response>()
{
  return robot_interfaces::srv::builder::Init_UpdateGaitParams_Response_success();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__SRV__DETAIL__UPDATE_GAIT_PARAMS__BUILDER_HPP_
