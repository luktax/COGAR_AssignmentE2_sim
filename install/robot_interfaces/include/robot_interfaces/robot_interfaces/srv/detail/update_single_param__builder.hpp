// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:srv/UpdateSingleParam.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__SRV__DETAIL__UPDATE_SINGLE_PARAM__BUILDER_HPP_
#define ROBOT_INTERFACES__SRV__DETAIL__UPDATE_SINGLE_PARAM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/srv/detail/update_single_param__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace srv
{

namespace builder
{

class Init_UpdateSingleParam_Request_value
{
public:
  explicit Init_UpdateSingleParam_Request_value(::robot_interfaces::srv::UpdateSingleParam_Request & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::srv::UpdateSingleParam_Request value(::robot_interfaces::srv::UpdateSingleParam_Request::_value_type arg)
  {
    msg_.value = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::srv::UpdateSingleParam_Request msg_;
};

class Init_UpdateSingleParam_Request_param_name
{
public:
  Init_UpdateSingleParam_Request_param_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_UpdateSingleParam_Request_value param_name(::robot_interfaces::srv::UpdateSingleParam_Request::_param_name_type arg)
  {
    msg_.param_name = std::move(arg);
    return Init_UpdateSingleParam_Request_value(msg_);
  }

private:
  ::robot_interfaces::srv::UpdateSingleParam_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::srv::UpdateSingleParam_Request>()
{
  return robot_interfaces::srv::builder::Init_UpdateSingleParam_Request_param_name();
}

}  // namespace robot_interfaces


namespace robot_interfaces
{

namespace srv
{

namespace builder
{

class Init_UpdateSingleParam_Response_message
{
public:
  explicit Init_UpdateSingleParam_Response_message(::robot_interfaces::srv::UpdateSingleParam_Response & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::srv::UpdateSingleParam_Response message(::robot_interfaces::srv::UpdateSingleParam_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::srv::UpdateSingleParam_Response msg_;
};

class Init_UpdateSingleParam_Response_success
{
public:
  Init_UpdateSingleParam_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_UpdateSingleParam_Response_message success(::robot_interfaces::srv::UpdateSingleParam_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_UpdateSingleParam_Response_message(msg_);
  }

private:
  ::robot_interfaces::srv::UpdateSingleParam_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::srv::UpdateSingleParam_Response>()
{
  return robot_interfaces::srv::builder::Init_UpdateSingleParam_Response_success();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__SRV__DETAIL__UPDATE_SINGLE_PARAM__BUILDER_HPP_
