// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robot_interfaces:srv/UpdateGaitParams.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__SRV__DETAIL__UPDATE_GAIT_PARAMS__STRUCT_HPP_
#define ROBOT_INTERFACES__SRV__DETAIL__UPDATE_GAIT_PARAMS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robot_interfaces__srv__UpdateGaitParams_Request __attribute__((deprecated))
#else
# define DEPRECATED__robot_interfaces__srv__UpdateGaitParams_Request __declspec(deprecated)
#endif

namespace robot_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct UpdateGaitParams_Request_
{
  using Type = UpdateGaitParams_Request_<ContainerAllocator>;

  explicit UpdateGaitParams_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frequency_hz = 0.0f;
      this->duty_cycle = 0.0f;
      this->height_swing = 0.0f;
    }
  }

  explicit UpdateGaitParams_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frequency_hz = 0.0f;
      this->duty_cycle = 0.0f;
      this->height_swing = 0.0f;
    }
  }

  // field types and members
  using _frequency_hz_type =
    float;
  _frequency_hz_type frequency_hz;
  using _duty_cycle_type =
    float;
  _duty_cycle_type duty_cycle;
  using _height_swing_type =
    float;
  _height_swing_type height_swing;
  using _phase_offset_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _phase_offset_type phase_offset;

  // setters for named parameter idiom
  Type & set__frequency_hz(
    const float & _arg)
  {
    this->frequency_hz = _arg;
    return *this;
  }
  Type & set__duty_cycle(
    const float & _arg)
  {
    this->duty_cycle = _arg;
    return *this;
  }
  Type & set__height_swing(
    const float & _arg)
  {
    this->height_swing = _arg;
    return *this;
  }
  Type & set__phase_offset(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->phase_offset = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_interfaces::srv::UpdateGaitParams_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_interfaces::srv::UpdateGaitParams_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_interfaces::srv::UpdateGaitParams_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_interfaces::srv::UpdateGaitParams_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::srv::UpdateGaitParams_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::srv::UpdateGaitParams_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::srv::UpdateGaitParams_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::srv::UpdateGaitParams_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_interfaces::srv::UpdateGaitParams_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_interfaces::srv::UpdateGaitParams_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_interfaces__srv__UpdateGaitParams_Request
    std::shared_ptr<robot_interfaces::srv::UpdateGaitParams_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_interfaces__srv__UpdateGaitParams_Request
    std::shared_ptr<robot_interfaces::srv::UpdateGaitParams_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const UpdateGaitParams_Request_ & other) const
  {
    if (this->frequency_hz != other.frequency_hz) {
      return false;
    }
    if (this->duty_cycle != other.duty_cycle) {
      return false;
    }
    if (this->height_swing != other.height_swing) {
      return false;
    }
    if (this->phase_offset != other.phase_offset) {
      return false;
    }
    return true;
  }
  bool operator!=(const UpdateGaitParams_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct UpdateGaitParams_Request_

// alias to use template instance with default allocator
using UpdateGaitParams_Request =
  robot_interfaces::srv::UpdateGaitParams_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace robot_interfaces


#ifndef _WIN32
# define DEPRECATED__robot_interfaces__srv__UpdateGaitParams_Response __attribute__((deprecated))
#else
# define DEPRECATED__robot_interfaces__srv__UpdateGaitParams_Response __declspec(deprecated)
#endif

namespace robot_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct UpdateGaitParams_Response_
{
  using Type = UpdateGaitParams_Response_<ContainerAllocator>;

  explicit UpdateGaitParams_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit UpdateGaitParams_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    robot_interfaces::srv::UpdateGaitParams_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_interfaces::srv::UpdateGaitParams_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_interfaces::srv::UpdateGaitParams_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_interfaces::srv::UpdateGaitParams_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::srv::UpdateGaitParams_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::srv::UpdateGaitParams_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::srv::UpdateGaitParams_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::srv::UpdateGaitParams_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_interfaces::srv::UpdateGaitParams_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_interfaces::srv::UpdateGaitParams_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_interfaces__srv__UpdateGaitParams_Response
    std::shared_ptr<robot_interfaces::srv::UpdateGaitParams_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_interfaces__srv__UpdateGaitParams_Response
    std::shared_ptr<robot_interfaces::srv::UpdateGaitParams_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const UpdateGaitParams_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const UpdateGaitParams_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct UpdateGaitParams_Response_

// alias to use template instance with default allocator
using UpdateGaitParams_Response =
  robot_interfaces::srv::UpdateGaitParams_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace robot_interfaces

namespace robot_interfaces
{

namespace srv
{

struct UpdateGaitParams
{
  using Request = robot_interfaces::srv::UpdateGaitParams_Request;
  using Response = robot_interfaces::srv::UpdateGaitParams_Response;
};

}  // namespace srv

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__SRV__DETAIL__UPDATE_GAIT_PARAMS__STRUCT_HPP_
