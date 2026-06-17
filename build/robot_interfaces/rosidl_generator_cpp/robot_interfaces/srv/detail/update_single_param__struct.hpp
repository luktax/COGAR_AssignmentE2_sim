// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robot_interfaces:srv/UpdateSingleParam.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__SRV__DETAIL__UPDATE_SINGLE_PARAM__STRUCT_HPP_
#define ROBOT_INTERFACES__SRV__DETAIL__UPDATE_SINGLE_PARAM__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robot_interfaces__srv__UpdateSingleParam_Request __attribute__((deprecated))
#else
# define DEPRECATED__robot_interfaces__srv__UpdateSingleParam_Request __declspec(deprecated)
#endif

namespace robot_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct UpdateSingleParam_Request_
{
  using Type = UpdateSingleParam_Request_<ContainerAllocator>;

  explicit UpdateSingleParam_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->param_name = "";
      this->value = 0.0f;
    }
  }

  explicit UpdateSingleParam_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : param_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->param_name = "";
      this->value = 0.0f;
    }
  }

  // field types and members
  using _param_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _param_name_type param_name;
  using _value_type =
    float;
  _value_type value;

  // setters for named parameter idiom
  Type & set__param_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->param_name = _arg;
    return *this;
  }
  Type & set__value(
    const float & _arg)
  {
    this->value = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_interfaces::srv::UpdateSingleParam_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_interfaces::srv::UpdateSingleParam_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_interfaces::srv::UpdateSingleParam_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_interfaces::srv::UpdateSingleParam_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::srv::UpdateSingleParam_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::srv::UpdateSingleParam_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::srv::UpdateSingleParam_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::srv::UpdateSingleParam_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_interfaces::srv::UpdateSingleParam_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_interfaces::srv::UpdateSingleParam_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_interfaces__srv__UpdateSingleParam_Request
    std::shared_ptr<robot_interfaces::srv::UpdateSingleParam_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_interfaces__srv__UpdateSingleParam_Request
    std::shared_ptr<robot_interfaces::srv::UpdateSingleParam_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const UpdateSingleParam_Request_ & other) const
  {
    if (this->param_name != other.param_name) {
      return false;
    }
    if (this->value != other.value) {
      return false;
    }
    return true;
  }
  bool operator!=(const UpdateSingleParam_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct UpdateSingleParam_Request_

// alias to use template instance with default allocator
using UpdateSingleParam_Request =
  robot_interfaces::srv::UpdateSingleParam_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace robot_interfaces


#ifndef _WIN32
# define DEPRECATED__robot_interfaces__srv__UpdateSingleParam_Response __attribute__((deprecated))
#else
# define DEPRECATED__robot_interfaces__srv__UpdateSingleParam_Response __declspec(deprecated)
#endif

namespace robot_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct UpdateSingleParam_Response_
{
  using Type = UpdateSingleParam_Response_<ContainerAllocator>;

  explicit UpdateSingleParam_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit UpdateSingleParam_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_interfaces::srv::UpdateSingleParam_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_interfaces::srv::UpdateSingleParam_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_interfaces::srv::UpdateSingleParam_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_interfaces::srv::UpdateSingleParam_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::srv::UpdateSingleParam_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::srv::UpdateSingleParam_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::srv::UpdateSingleParam_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::srv::UpdateSingleParam_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_interfaces::srv::UpdateSingleParam_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_interfaces::srv::UpdateSingleParam_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_interfaces__srv__UpdateSingleParam_Response
    std::shared_ptr<robot_interfaces::srv::UpdateSingleParam_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_interfaces__srv__UpdateSingleParam_Response
    std::shared_ptr<robot_interfaces::srv::UpdateSingleParam_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const UpdateSingleParam_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const UpdateSingleParam_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct UpdateSingleParam_Response_

// alias to use template instance with default allocator
using UpdateSingleParam_Response =
  robot_interfaces::srv::UpdateSingleParam_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace robot_interfaces

namespace robot_interfaces
{

namespace srv
{

struct UpdateSingleParam
{
  using Request = robot_interfaces::srv::UpdateSingleParam_Request;
  using Response = robot_interfaces::srv::UpdateSingleParam_Response;
};

}  // namespace srv

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__SRV__DETAIL__UPDATE_SINGLE_PARAM__STRUCT_HPP_
