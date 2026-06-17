// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robot_interfaces:srv/UpdateGaitParams.idl
// generated code does not contain a copyright notice

#ifndef ROBOT_INTERFACES__SRV__DETAIL__UPDATE_GAIT_PARAMS__TRAITS_HPP_
#define ROBOT_INTERFACES__SRV__DETAIL__UPDATE_GAIT_PARAMS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robot_interfaces/srv/detail/update_gait_params__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace robot_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const UpdateGaitParams_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: frequency_hz
  {
    out << "frequency_hz: ";
    rosidl_generator_traits::value_to_yaml(msg.frequency_hz, out);
    out << ", ";
  }

  // member: duty_cycle
  {
    out << "duty_cycle: ";
    rosidl_generator_traits::value_to_yaml(msg.duty_cycle, out);
    out << ", ";
  }

  // member: height_swing
  {
    out << "height_swing: ";
    rosidl_generator_traits::value_to_yaml(msg.height_swing, out);
    out << ", ";
  }

  // member: phase_offset
  {
    if (msg.phase_offset.size() == 0) {
      out << "phase_offset: []";
    } else {
      out << "phase_offset: [";
      size_t pending_items = msg.phase_offset.size();
      for (auto item : msg.phase_offset) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const UpdateGaitParams_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: frequency_hz
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "frequency_hz: ";
    rosidl_generator_traits::value_to_yaml(msg.frequency_hz, out);
    out << "\n";
  }

  // member: duty_cycle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "duty_cycle: ";
    rosidl_generator_traits::value_to_yaml(msg.duty_cycle, out);
    out << "\n";
  }

  // member: height_swing
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "height_swing: ";
    rosidl_generator_traits::value_to_yaml(msg.height_swing, out);
    out << "\n";
  }

  // member: phase_offset
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.phase_offset.size() == 0) {
      out << "phase_offset: []\n";
    } else {
      out << "phase_offset:\n";
      for (auto item : msg.phase_offset) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const UpdateGaitParams_Request & msg, bool use_flow_style = false)
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
  const robot_interfaces::srv::UpdateGaitParams_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  robot_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robot_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const robot_interfaces::srv::UpdateGaitParams_Request & msg)
{
  return robot_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<robot_interfaces::srv::UpdateGaitParams_Request>()
{
  return "robot_interfaces::srv::UpdateGaitParams_Request";
}

template<>
inline const char * name<robot_interfaces::srv::UpdateGaitParams_Request>()
{
  return "robot_interfaces/srv/UpdateGaitParams_Request";
}

template<>
struct has_fixed_size<robot_interfaces::srv::UpdateGaitParams_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<robot_interfaces::srv::UpdateGaitParams_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<robot_interfaces::srv::UpdateGaitParams_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace robot_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const UpdateGaitParams_Response & msg,
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
  const UpdateGaitParams_Response & msg,
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

inline std::string to_yaml(const UpdateGaitParams_Response & msg, bool use_flow_style = false)
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
  const robot_interfaces::srv::UpdateGaitParams_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  robot_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robot_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const robot_interfaces::srv::UpdateGaitParams_Response & msg)
{
  return robot_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<robot_interfaces::srv::UpdateGaitParams_Response>()
{
  return "robot_interfaces::srv::UpdateGaitParams_Response";
}

template<>
inline const char * name<robot_interfaces::srv::UpdateGaitParams_Response>()
{
  return "robot_interfaces/srv/UpdateGaitParams_Response";
}

template<>
struct has_fixed_size<robot_interfaces::srv::UpdateGaitParams_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<robot_interfaces::srv::UpdateGaitParams_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<robot_interfaces::srv::UpdateGaitParams_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<robot_interfaces::srv::UpdateGaitParams>()
{
  return "robot_interfaces::srv::UpdateGaitParams";
}

template<>
inline const char * name<robot_interfaces::srv::UpdateGaitParams>()
{
  return "robot_interfaces/srv/UpdateGaitParams";
}

template<>
struct has_fixed_size<robot_interfaces::srv::UpdateGaitParams>
  : std::integral_constant<
    bool,
    has_fixed_size<robot_interfaces::srv::UpdateGaitParams_Request>::value &&
    has_fixed_size<robot_interfaces::srv::UpdateGaitParams_Response>::value
  >
{
};

template<>
struct has_bounded_size<robot_interfaces::srv::UpdateGaitParams>
  : std::integral_constant<
    bool,
    has_bounded_size<robot_interfaces::srv::UpdateGaitParams_Request>::value &&
    has_bounded_size<robot_interfaces::srv::UpdateGaitParams_Response>::value
  >
{
};

template<>
struct is_service<robot_interfaces::srv::UpdateGaitParams>
  : std::true_type
{
};

template<>
struct is_service_request<robot_interfaces::srv::UpdateGaitParams_Request>
  : std::true_type
{
};

template<>
struct is_service_response<robot_interfaces::srv::UpdateGaitParams_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // ROBOT_INTERFACES__SRV__DETAIL__UPDATE_GAIT_PARAMS__TRAITS_HPP_
