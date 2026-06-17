import sys
import rclpy
from go2_rl_controller.rl_controller_node import RLControllerNode

def main():
    if len(sys.argv) < 2:
        print("Usage: python load_policy.py <path_to_policy.pt>")
        sys.exit(1)
    
    policy_path = sys.argv[1]
    
    rclpy.init()
    node = RLControllerNode()
    
    # Carica la policy
    success = node.load_policy(policy_path)
    
    if success:
        print(f"✓ Policy caricata da: {policy_path}")
        print("Node in ascolto...")
        rclpy.spin(node)
    else:
        print(f"✗ Errore nel caricamento della policy")
        sys.exit(1)
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()