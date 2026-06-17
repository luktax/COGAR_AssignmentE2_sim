// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robot_interfaces:srv/SetBodyHeight.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__SRV__DETAIL__SET_BODY_HEIGHT__TRAITS_HPP_
#define ROBOT_INTERFACES__SRV__DETAIL__SET_BODY_HEIGHT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robot_interfaces/srv/detail/set_body_height__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace robot_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetBodyHeight_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: height
  {
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetBodyHeight_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetBodyHeight_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace robot_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use robot_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const robot_interfaces::srv::SetBodyHeight_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  robot_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robot_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const robot_interfaces::srv::SetBodyHeight_Request & msg)
{
  return robot_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<robot_interfaces::srv::SetBodyHeight_Request>()
{
  return "robot_interfaces::srv::SetBodyHeight_Request";
}

template<>
inline const char * name<robot_interfaces::srv::SetBodyHeight_Request>()
{
  return "robot_interfaces/srv/SetBodyHeight_Request";
}

template<>
struct has_fixed_size<robot_interfaces::srv::SetBodyHeight_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<robot_interfaces::srv::SetBodyHeight_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<robot_interfaces::srv::SetBodyHeight_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace robot_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetBodyHeight_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetBodyHeight_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetBodyHeight_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace robot_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use robot_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const robot_interfaces::srv::SetBodyHeight_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  robot_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robot_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const robot_interfaces::srv::SetBodyHeight_Response & msg)
{
  return robot_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<robot_interfaces::srv::SetBodyHeight_Response>()
{
  return "robot_interfaces::srv::SetBodyHeight_Response";
}

template<>
inline const char * name<robot_interfaces::srv::SetBodyHeight_Response>()
{
  return "robot_interfaces/srv/SetBodyHeight_Response";
}

template<>
struct has_fixed_size<robot_interfaces::srv::SetBodyHeight_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<robot_interfaces::srv::SetBodyHeight_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<robot_interfaces::srv::SetBodyHeight_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<robot_interfaces::srv::SetBodyHeight>()
{
  return "robot_interfaces::srv::SetBodyHeight";
}

template<>
inline const char * name<robot_interfaces::srv::SetBodyHeight>()
{
  return "robot_interfaces/srv/SetBodyHeight";
}

template<>
struct has_fixed_size<robot_interfaces::srv::SetBodyHeight>
  : std::integral_constant<
    bool,
    has_fixed_size<robot_interfaces::srv::SetBodyHeight_Request>::value &&
    has_fixed_size<robot_interfaces::srv::SetBodyHeight_Response>::value
  >
{
};

template<>
struct has_bounded_size<robot_interfaces::srv::SetBodyHeight>
  : std::integral_constant<
    bool,
    has_bounded_size<robot_interfaces::srv::SetBodyHeight_Request>::value &&
    has_bounded_size<robot_interfaces::srv::SetBodyHeight_Response>::value
  >
{
};

template<>
struct is_service<robot_interfaces::srv::SetBodyHeight>
  : std::true_type
{
};

template<>
struct is_service_request<robot_interfaces::srv::SetBodyHeight_Request>
  : std::true_type
{
};

template<>
struct is_service_response<robot_interfaces::srv::SetBodyHeight_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // ROBOT_INTERFACES__SRV__DETAIL__SET_BODY_HEIGHT__TRAITS_HPP_
