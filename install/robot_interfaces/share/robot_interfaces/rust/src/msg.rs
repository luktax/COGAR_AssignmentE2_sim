#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to robot_interfaces__msg__RobotState

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub q: [f64; 19],


    // This member is not documented.
    #[allow(missing_docs)]
    pub dq: [f64; 18],


    // This member is not documented.
    #[allow(missing_docs)]
    pub imu_quat: [f64; 4],


    // This member is not documented.
    #[allow(missing_docs)]
    pub imu_gyro: [f64; 3],


    // This member is not documented.
    #[allow(missing_docs)]
    pub time: f64,

}



impl Default for RobotState {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RobotState::default())
  }
}

impl rosidl_runtime_rs::Message for RobotState {
  type RmwMsg = super::msg::rmw::RobotState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        q: msg.q,
        dq: msg.dq,
        imu_quat: msg.imu_quat,
        imu_gyro: msg.imu_gyro,
        time: msg.time,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        q: msg.q,
        dq: msg.dq,
        imu_quat: msg.imu_quat,
        imu_gyro: msg.imu_gyro,
      time: msg.time,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      q: msg.q,
      dq: msg.dq,
      imu_quat: msg.imu_quat,
      imu_gyro: msg.imu_gyro,
      time: msg.time,
    }
  }
}


