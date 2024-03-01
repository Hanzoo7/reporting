#s.fauquembergue(sii)
#v1.0
#initial release 25/10/2023

from ansible.module_utils.basic import AnsibleModule
import sys, os
from openpyxl import Workbook

def main():
    #region params
    module_args = dict(
        workbook = dict(required=True, type='str'),
        )

    #endregion

    #region ansible
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    workbook = module.params.get('workbook')

    result = dict(
        changed=False,
        skipped=True,
        message=None
    )
    #endregion

    #region get
    output=workbook
    result["message"]=output
    result["skipped"]=False
    #endregion

    #region test
    compliant=True
    
    if not os.path.exists(workbook):
        compliant=False

    if module.check_mode:
        module.exit_json(**result)
    #endregion

    #region set
    if not compliant:
        wb=Workbook()
        wb.save(workbook)
        result["changed"]=True
    #endregion

    module.exit_json(**result)

if __name__ == '__main__':
    main()

