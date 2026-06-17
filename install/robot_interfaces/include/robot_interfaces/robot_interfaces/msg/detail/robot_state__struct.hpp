// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robot_interfaces:msg/RobotState.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__MSG__DETAIL__ROBOT_STATE__STRUCT_HPP_
#define ROBOT_INTERFACES__MSG__DETAIL__ROBOT_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__robot_interfaces__msg__RobotState __attribute__((deprecated))
#else
# define DEPRECATED__robot_interfaces__msg__RobotState __declspec(deprecated)
#endif

namespace robot_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct RobotState_
{
  using Type = RobotState_<ContainerAllocator>;

  explicit RobotState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 19>::iterator, double>(this->q.begin(), this->q.end(), 0.0);
      std::fill<typename std::array<double, 18>::iterator, double>(this->dq.begin(), this->dq.end(), 0.0);
      std::fill<typename std::array<double, 4>::iterator, double>(this->imu_quat.begin(), this->imu_quat.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->imu_gyro.begin(), this->imu_gyro.end(), 0.0);
      this->time = 0.0;
    }
  }

  explicit RobotState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    q(_alloc),
    dq(_alloc),
    imu_quat(_alloc),
    imu_gyro(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 19>::iterator, double>(this->q.begin(), this->q.end(), 0.0);
      std::fill<typename std::array<double, 18>::iterator, double>(this->dq.begin(), this->dq.end(), 0.0);
      std::fill<typename std::array<double, 4>::iterator, double>(this->imu_quat.begin(), this->imu_quat.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->imu_gyro.begin(), this->imu_gyro.end(), 0.0);
      this->time = 0.0;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _q_type =
    std::array<double, 19>;
  _q_type q;
  using _dq_type =
    std::array<double, 18>;
  _dq_type dq;
  using _imu_quat_type =
    std::array<double, 4>;
  _imu_quat_type imu_quat;
  using _imu_gyro_type =
    std::array<double, 3>;
  _imu_gyro_type imu_gyro;
  using _time_type =
    double;
  _time_type time;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__q(
    const std::array<double, 19> & _arg)
  {
    this->q = _arg;
    return *this;
  }
  Type & set__dq(
    const std::array<double, 18> & _arg)
  {
    this->dq = _arg;
    return *this;
  }
  Type & set__imu_quat(
    const std::array<double, 4> & _arg)
  {
    this->imu_quat = _arg;
    return *this;
  }
  Type & set__imu_gyro(
    const std::array<double, 3> & _arg)
  {
    this->imu_gyro = _arg;
    return *this;
  }
  Type & set__time(
    const double & _arg)
  {
    this->time = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robot_interfaces::msg::RobotState_<ContainerAllocator> *;
  using ConstRawPtr =
    const robot_interfaces::msg::RobotState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robot_interfaces::msg::RobotState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robot_interfaces::msg::RobotState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::msg::RobotState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::msg::RobotState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robot_interfaces::msg::RobotState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robot_interfaces::msg::RobotState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robot_interfaces::msg::RobotState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robot_interfaces::msg::RobotState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robot_interfaces__msg__RobotState
    std::shared_ptr<robot_interfaces::msg::RobotState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robot_interfaces__msg__RobotState
    std::shared_ptr<robot_interfaces::msg::RobotState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RobotState_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->q != other.q) {
      return false;
    }
    if (this->dq != other.dq) {
      return false;
    }
    if (this->imu_quat != other.imu_quat) {
      return false;
    }
    if (this->imu_gyro != other.imu_gyro) {
      return false;
    }
    if (this->time != other.time) {
      return false;
    }
    return true;
  }
  bool operator!=(const RobotState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RobotState_

// alias to use template instance with default allocator
using RobotState =
  robot_interfaces::msg::RobotState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robot_interfaces

#endif  // ROBOT_INTERFACES__MSG__DETAIL__ROBOT_STATE__STRUCT_HPP_
