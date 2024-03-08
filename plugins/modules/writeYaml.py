#s.fauquembergue(sii)
#v1.0
#initial release 08/03/2024

#known issue
# unexpected yaml format provided behavior when datas exceed 1000 lines

from ansible.module_utils.basic import AnsibleModule
from deepdiff import DeepDiff, Delta
import os, sys, yaml

def get_resources(node, dest):
    if not os.path.exists(dest):
        nodeDatas = {}
    else:
        nodeDatas=yaml.safe_load((open(dest, 'r')).read())
    
    for n in node.split('/'):
        if not nodeDatas:
            nodeDatas = {}
        
        if n not in nodeDatas.keys():
            nodeDatas[n] = {}
        
        nodeDatas=nodeDatas[n]
    
    return nodeDatas

def test_resources(destNodeDatas, insert) :
    diff = DeepDiff(destNodeDatas, insert, ignore_order=True, report_repetition=True)
    return diff

def set_resources(insert, node, dest, diff):
    if not os.path.exists(dest):
        open(dest, 'w').close()

    nodeDatas_r = yaml.safe_load((open(dest, 'r')).read())
    position = "nodeDatas_r"

    if not nodeDatas_r:
        nodeDatas_r = {}
        

    for n in node.split('/'):
        exec("if not "+position+":"+position+"={}") 
        exec("if '"+n+"' not in "+position+".keys():"+position+"['"+n+"']={}")    
        position = position+"['"+n+"']"
        
    exec(position+"=insert")

    
    nodeDatas_w = open(dest, 'w')

        
    yaml.dump(nodeDatas_r, nodeDatas_w, default_flow_style=False, encoding = "utf-8", allow_unicode=True)
    #nodeDatas_w.write(str(objet_python))





    nodeDatas_w.close()
    return dict(diff)

def main():
    #region params
    module_args = dict(
        node = dict(required=True, type='str'),
        insertlist = dict(required=False, type='list'),
        insertdict = dict(required=False, type='dict'),
        dest = dict(required=True, type='str'),
        )
    #endregion

    #region ansible
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    node = module.params.get('node')
    insertlist = module.params.get('insertlist')
    insertdict = module.params.get('insertdict')
    dest = module.params.get('dest')

    if insertlist:
        insert = insertlist
    elif insertdict:
        insert = insertdict

    result = dict(
        changed=False,
        skipped=False,
        message=None
    )
    #endregion

    try:       
        destNodeDatas = get_resources(node, dest)
        result['message'] = 'Compliant'
        diff = test_resources(destNodeDatas, insert)
        
        if module.check_mode:
            result['skipped'] = True
            module.exit_json(**result)        

        if diff != {}:
            set = set_resources(insert, node, dest, diff)
            result['message'] = set
            result['changed'] = True

    except:
        result['message'] = sys.exc_info()[1]

    finally:
        module.exit_json(**result)

if __name__ == '__main__':
    main()

