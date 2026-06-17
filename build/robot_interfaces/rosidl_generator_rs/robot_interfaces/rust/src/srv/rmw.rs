#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "robot_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__robot_interfaces__srv__UpdateGaitParams_Request() -> *const std::ffi::c_void;
}

#[link(name = "robot_interfaces__rosidl_generator_c")]
extern "C" {
    fn robot_interfaces__srv__UpdateGaitParams_Request__init(msg: *mut UpdateGaitParams_Request) -> bool;
    fn robot_interfaces__srv__UpdateGaitParams_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<UpdateGaitParams_Request>, size: usize) -> bool;
    fn robot_interfaces__srv__UpdateGaitParams_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<UpdateGaitParams_Request>);
    fn robot_interfaces__srv__UpdateGaitParams_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<UpdateGaitParams_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<UpdateGaitParams_Request>) -> bool;
}

// Corresponds to robot_interfaces__srv__UpdateGaitParams_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    pub phase_offset: rosidl_runtime_rs::Sequence<f32>,

}



impl Default for UpdateGaitParams_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !robot_interfaces__srv__UpdateGaitParams_Request__init(&mut msg as *mut _) {
        panic!("Call to robot_interfaces__srv__UpdateGaitParams_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for UpdateGaitParams_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__UpdateGaitParams_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__UpdateGaitParams_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__UpdateGaitParams_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for UpdateGaitParams_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for UpdateGaitParams_Request where Self: Sized {
  const TYPE_NAME: &'static str = "robot_interfaces/srv/UpdateGaitParams_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__robot_interfaces__srv__UpdateGaitParams_Request() }
  }
}


#[link(name = "robot_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__robot_interfaces__srv__UpdateGaitParams_Response() -> *const std::ffi::c_void;
}

#[link(name = "robot_interfaces__rosidl_generator_c")]
extern "C" {
    fn robot_interfaces__srv__UpdateGaitParams_Response__init(msg: *mut UpdateGaitParams_Response) -> bool;
    fn robot_interfaces__srv__UpdateGaitParams_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<UpdateGaitParams_Response>, size: usize) -> bool;
    fn robot_interfaces__srv__UpdateGaitParams_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<UpdateGaitParams_Response>);
    fn robot_interfaces__srv__UpdateGaitParams_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<UpdateGaitParams_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<UpdateGaitParams_Response>) -> bool;
}

// Corresponds to robot_interfaces__srv__UpdateGaitParams_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct UpdateGaitParams_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for UpdateGaitParams_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !robot_interfaces__srv__UpdateGaitParams_Response__init(&mut msg as *mut _) {
        panic!("Call to robot_interfaces__srv__UpdateGaitParams_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for UpdateGaitParams_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__UpdateGaitParams_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__UpdateGaitParams_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__UpdateGaitParams_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for UpdateGaitParams_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for UpdateGaitParams_Response where Self: Sized {
  const TYPE_NAME: &'static str = "robot_interfaces/srv/UpdateGaitParams_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__robot_interfaces__srv__UpdateGaitParams_Response() }
  }
}


#[link(name = "robot_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__robot_interfaces__srv__UpdateSingleParam_Request() -> *const std::ffi::c_void;
}

#[link(name = "robot_interfaces__rosidl_generator_c")]
extern "C" {
    fn robot_interfaces__srv__UpdateSingleParam_Request__init(msg: *mut UpdateSingleParam_Request) -> bool;
    fn robot_interfaces__srv__UpdateSingleParam_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<UpdateSingleParam_Request>, size: usize) -> bool;
    fn robot_interfaces__srv__UpdateSingleParam_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<UpdateSingleParam_Request>);
    fn robot_interfaces__srv__UpdateSingleParam_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<UpdateSingleParam_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<UpdateSingleParam_Request>) -> bool;
}

// Corresponds to robot_interfaces__srv__UpdateSingleParam_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct UpdateSingleParam_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub param_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: f32,

}



impl Default for UpdateSingleParam_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !robot_interfaces__srv__UpdateSingleParam_Request__init(&mut msg as *mut _) {
        panic!("Call to robot_interfaces__srv__UpdateSingleParam_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for UpdateSingleParam_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__UpdateSingleParam_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__UpdateSingleParam_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__UpdateSingleParam_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for UpdateSingleParam_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for UpdateSingleParam_Request where Self: Sized {
  const TYPE_NAME: &'static str = "robot_interfaces/srv/UpdateSingleParam_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__robot_interfaces__srv__UpdateSingleParam_Request() }
  }
}


#[link(name = "robot_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__robot_interfaces__srv__UpdateSingleParam_Response() -> *const std::ffi::c_void;
}

#[link(name = "robot_interfaces__rosidl_generator_c")]
extern "C" {
    fn robot_interfaces__srv__UpdateSingleParam_Response__init(msg: *mut UpdateSingleParam_Response) -> bool;
    fn robot_interfaces__srv__UpdateSingleParam_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<UpdateSingleParam_Response>, size: usize) -> bool;
    fn robot_interfaces__srv__UpdateSingleParam_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<UpdateSingleParam_Response>);
    fn robot_interfaces__srv__UpdateSingleParam_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<UpdateSingleParam_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<UpdateSingleParam_Response>) -> bool;
}

// Corresponds to robot_interfaces__srv__UpdateSingleParam_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct UpdateSingleParam_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for UpdateSingleParam_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !robot_interfaces__srv__UpdateSingleParam_Response__init(&mut msg as *mut _) {
        panic!("Call to robot_interfaces__srv__UpdateSingleParam_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for UpdateSingleParam_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__UpdateSingleParam_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__UpdateSingleParam_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__UpdateSingleParam_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for UpdateSingleParam_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for UpdateSingleParam_Response where Self: Sized {
  const TYPE_NAME: &'static str = "robot_interfaces/srv/UpdateSingleParam_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__robot_interfaces__srv__UpdateSingleParam_Response() }
  }
}


#[link(name = "robot_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__robot_interfaces__srv__SetBodyHeight_Request() -> *const std::ffi::c_void;
}

#[link(name = "robot_interfaces__rosidl_generator_c")]
extern "C" {
    fn robot_interfaces__srv__SetBodyHeight_Request__init(msg: *mut SetBodyHeight_Request) -> bool;
    fn robot_interfaces__srv__SetBodyHeight_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetBodyHeight_Request>, size: usize) -> bool;
    fn robot_interfaces__srv__SetBodyHeight_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetBodyHeight_Request>);
    fn robot_interfaces__srv__SetBodyHeight_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetBodyHeight_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetBodyHeight_Request>) -> bool;
}

// Corresponds to robot_interfaces__srv__SetBodyHeight_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetBodyHeight_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub height: f32,

}



impl Default for SetBodyHeight_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !robot_interfaces__srv__SetBodyHeight_Request__init(&mut msg as *mut _) {
        panic!("Call to robot_interfaces__srv__SetBodyHeight_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetBodyHeight_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__SetBodyHeight_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__SetBodyHeight_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__SetBodyHeight_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetBodyHeight_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetBodyHeight_Request where Self: Sized {
  const TYPE_NAME: &'static str = "robot_interfaces/srv/SetBodyHeight_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__robot_interfaces__srv__SetBodyHeight_Request() }
  }
}


#[link(name = "robot_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__robot_interfaces__srv__SetBodyHeight_Response() -> *const std::ffi::c_void;
}

#[link(name = "robot_interfaces__rosidl_generator_c")]
extern "C" {
    fn robot_interfaces__srv__SetBodyHeight_Response__init(msg: *mut SetBodyHeight_Response) -> bool;
    fn robot_interfaces__srv__SetBodyHeight_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetBodyHeight_Response>, size: usize) -> bool;
    fn robot_interfaces__srv__SetBodyHeight_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetBodyHeight_Response>);
    fn robot_interfaces__srv__SetBodyHeight_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetBodyHeight_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetBodyHeight_Response>) -> bool;
}

// Corresponds to robot_interfaces__srv__SetBodyHeight_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetBodyHeight_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for SetBodyHeight_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !robot_interfaces__srv__SetBodyHeight_Response__init(&mut msg as *mut _) {
        panic!("Call to robot_interfaces__srv__SetBodyHeight_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetBodyHeight_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__SetBodyHeight_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__SetBodyHeight_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robot_interfaces__srv__SetBodyHeight_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetBodyHeight_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetBodyHeight_Response where Self: Sized {
  const TYPE_NAME: &'static str = "robot_interfaces/srv/SetBodyHeight_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__robot_interfaces__srv__SetBodyHeight_Response() }
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


