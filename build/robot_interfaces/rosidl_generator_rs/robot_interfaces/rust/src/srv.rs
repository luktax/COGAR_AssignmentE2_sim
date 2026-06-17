#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to robot_interfaces__srv__UpdateGaitParams_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct UpdateGaitParams_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub frequency_hz: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub duty_cycle: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub height_swing: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub phase_offset: Vec<f32>,

}



impl Default for UpdateGaitParams_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::UpdateGaitParams_Request::default())
  }
}

impl rosidl_runtime_rs::Message for UpdateGaitParams_Request {
  type RmwMsg = super::srv::rmw::UpdateGaitParams_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        frequency_hz: msg.frequency_hz,
        duty_cycle: msg.duty_cycle,
        height_swing: msg.height_swing,
        phase_offset: msg.phase_offset.into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      frequency_hz: msg.frequency_hz,
      duty_cycle: msg.duty_cycle,
      height_swing: msg.height_swing,
        phase_offset: msg.phase_offset.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      frequency_hz: msg.frequency_hz,
      duty_cycle: msg.duty_cycle,
      height_swing: msg.height_swing,
      phase_offset: msg.phase_offset
          .into_iter()
          .collect(),
    }
  }
}


// Corresponds to robot_interfaces__srv__UpdateGaitParams_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct UpdateGaitParams_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for UpdateGaitParams_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::UpdateGaitParams_Response::default())
  }
}

impl rosidl_runtime_rs::Message for UpdateGaitParams_Response {
  type RmwMsg = super::srv::rmw::UpdateGaitParams_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to robot_interfaces__srv__UpdateSingleParam_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct UpdateSingleParam_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub param_name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: f32,

}



impl Default for UpdateSingleParam_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::UpdateSingleParam_Request::default())
  }
}

impl rosidl_runtime_rs::Message for UpdateSingleParam_Request {
  type RmwMsg = super::srv::rmw::UpdateSingleParam_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        param_name: msg.param_name.as_str().into(),
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        param_name: msg.param_name.as_str().into(),
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      param_name: msg.param_name.to_string(),
      value: msg.value,
    }
  }
}


// Corresponds to robot_interfaces__srv__UpdateSingleParam_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct UpdateSingleParam_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for UpdateSingleParam_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::UpdateSingleParam_Response::default())
  }
}

impl rosidl_runtime_rs::Message for UpdateSingleParam_Response {
  type RmwMsg = super::srv::rmw::UpdateSingleParam_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to robot_interfaces__srv__SetBodyHeight_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetBodyHeight_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub height: f32,

}



impl Default for SetBodyHeight_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetBodyHeight_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetBodyHeight_Request {
  type RmwMsg = super::srv::rmw::SetBodyHeight_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        height: msg.height,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      height: msg.height,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      height: msg.height,
    }
  }
}


// Corresponds to robot_interfaces__srv__SetBodyHeight_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetBodyHeight_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for SetBodyHeight_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetBodyHeight_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetBodyHeight_Response {
  type RmwMsg = super::srv::rmw::SetBodyHeight_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}






#[link(name = "robot_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__robot_interfaces__srv__UpdateGaitParams() -> *const std::ffi::c_void;
}

// Corresponds to robot_interfaces__srv__UpdateGaitParams
#[allow(missing_docs, non_camel_case_types)]
pub struct UpdateGaitParams;

impl rosidl_runtime_rs::Service for UpdateGaitParams {
    type Request = UpdateGaitParams_Request;
    type Response = UpdateGaitParams_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__robot_interfaces__srv__UpdateGaitParams() }
    }
}




#[link(name = "robot_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__robot_interfaces__srv__UpdateSingleParam() -> *const std::ffi::c_void;
}

// Corresponds to robot_interfaces__srv__UpdateSingleParam
#[allow(missing_docs, non_camel_case_types)]
pub struct UpdateSingleParam;

impl rosidl_runtime_rs::Service for UpdateSingleParam {
    type Request = UpdateSingleParam_Request;
    type Response = UpdateSingleParam_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__robot_interfaces__srv__UpdateSingleParam() }
    }
}




#[link(name = "robot_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__robot_interfaces__srv__SetBodyHeight() -> *const std::ffi::c_void;
}

// Corresponds to robot_interfaces__srv__SetBodyHeight
#[allow(missing_docs, non_camel_case_types)]
pub struct SetBodyHeight;

impl rosidl_runtime_rs::Service for SetBodyHeight {
    type Request = SetBodyHeight_Request;
    type Response = SetBodyHeight_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__robot_interfaces__srv__SetBodyHeight() }
    }
}


