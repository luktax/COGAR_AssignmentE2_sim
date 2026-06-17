// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robot_interfaces:srv/SetBodyHeight.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__SRV__DETAIL__SET_BODY_HEIGHT__BUILDER_HPP_
#define ROBOT_INTERFACES__SRV__DETAIL__SET_BODY_HEIGHT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robot_interfaces/srv/detail/set_body_height__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robot_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetBodyHeight_Request_height
{
public:
  Init_SetBodyHeight_Request_height()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::robot_interfaces::srv::SetBodyHeight_Request height(::robot_interfaces::srv::SetBodyHeight_Request::_height_type arg)
  {
    msg_.height = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::srv::SetBodyHeight_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::srv::SetBodyHeight_Request>()
{
  return robot_interfaces::srv::builder::Init_SetBodyHeight_Request_height();
}

}  // namespace robot_interfaces


namespace robot_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetBodyHeight_Response_message
{
public:
  explicit Init_SetBodyHeight_Response_message(::robot_interfaces::srv::SetBodyHeight_Response & msg)
  : msg_(msg)
  {}
  ::robot_interfaces::srv::SetBodyHeight_Response message(::robot_interfaces::srv::SetBodyHeight_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robot_interfaces::srv::SetBodyHeight_Response msg_;
};

class Init_SetBodyHeight_Response_success
{
public:
  Init_SetBodyHeight_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetBodyHeight_Response_message success(::robot_interfaces::srv::SetBodyHeight_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_SetBodyHeight_Response_message(msg_);
  }

private:
  ::robot_interfaces::srv::SetBodyHeight_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::robot_interfaces::srv::SetBodyHeight_Response>()
{
  return robot_interfaces::srv::builder::Init_SetBodyHeight_Response_success();
}

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__SRV__DETAIL__SET_BODY_HEIGHT__BUILDER_HPP_
