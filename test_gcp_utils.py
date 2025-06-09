# test_gcp_utils.py
from app.utils.gcp_utils import create_instance , get_instance_external_ip
import time

if __name__ == "__main__":
    TEST_REPO = "https://github.com/SwayamY/sample-docker-multicontainer-for-testing.git"
    try:
        result = create_instance(TEST_REPO)
        vm_name =  result["vm_name"]
        time.sleep(10)
        external_ip = get_instance_external_ip(vm_name)


        print("[✅ SUCCESS] VM creation triggered.")
        print(result)
        print({"VM_Name": vm_name,
            "External_IP": external_ip or "pending"})
    except Exception as e:
        print("[❌ ERROR]", str(e))
