#s.fauquembergue(sii)
#v1.0
#initial release 04/03/2024

from ansible.module_utils.basic import AnsibleModule
from deepdiff import DeepDiff, Delta
import os, sys, yaml

def get_resources(dest, nodeName):
    nodecontent = None
    destcontent = None
    
    if os.path.exists(dest):
        destcontent=yaml.safe_load((open(dest, 'r')).read())
        
        if nodeName in destcontent.keys():
            nodecontent=destcontent[nodeName]

    return nodecontent

def test_resources(get,ref):
    diff=DeepDiff(get, ref ,ignore_order=True, report_repetition=True)
    return diff

def set_resources(ref, dest, diff, nodeName):
    destcontent=yaml.safe_load((open(dest, 'r')).read())
    destcontent.update({nodeName:ref})


    #Write to file



    return destcontent

def main():
    #region params
    module_args = dict(
        nodeName = dict(required=True, type='str'),
        content = dict(required=True, type='dict'),
        dest = dict(required=True, type='str'),
        )
    #endregion

    #region ansible
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    nodeName = module.params.get('nodeName')
    content = module.params.get('content')
    dest = module.params.get('dest')

    result = dict(
        changed=False,
        skipped=False,
        message=None
    )
    #endregion

    try:       
        get = get_resources(dest, nodeName)
        result['message']=get
        test = test_resources(get=get,ref=content)
        
        if module.check_mode:
            result['skipped'] = True
            module.exit_json(**result)        

        if test != {}:
            set = set_resources(content, dest, test, nodeName)
            result['message'] = set
            result['changed'] = True

    except:
        result['message'] = sys.exc_info()[1]

    finally:
        module.exit_json(**result)

if __name__ == '__main__':
    main()

