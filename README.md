# Skeleton
## Structure
[main.yml](playbooks%2Fmain.yml):
- fetch configs from all servers and convert them into tasks (role [fetch_config](playbooks%2Froles%2Ffetch_config))
- Handle each task (role [process_task](playbooks%2Froles%2Fprocess_task))

[process_task](playbooks%2Froles%2Fprocess_task):
- Initialize change flag to False (will be evaluated to know if notif should be sent)
- Get NPAs passwords from cyberark (role [get_npa_password](playbooks%2Froles%2Fget_npa_password))
- Update NPAs in .profile if needed (role [update_npa_file](playbooks%2Froles%2Fupdate_npa_file))
- Restart module if restart command provided and .profile was updated (role [restart_module](playbooks%2Froles%2Frestart_module))
- Send mail notification if restart command provided and restart successful, or if .profile changed (role [send_mail](playbooks%2Froles%2Fsend_mail))
- Send error mail if any part failed (role [send_mail](playbooks%2Froles%2Fsend_mail))

[fetch_config](playbooks%2Froles%2Ffetch_config):
- Cleanup old directories
- Fetch configurations on server
- Transform them into a list of tasks using [generate_tasks.py](playbooks%2Froles%2Ffetch_config%2Ffiles%2Fgenerate_tasks.py)

## TODO
- [main.yml](playbooks%2Fmain.yml) -> should be ok
- [fetch_config](playbooks%2Froles%2Ffetch_config) -> adapt to go on remote server + send mail if config parsing error occurred
- [get_npa_password](playbooks%2Froles%2Fget_npa_password) -> everything ! 
  - Need to call cyberark to check if NPA pass should be changed
  - If expires soon, update it
  - Return the NPA password
- [restart_module](playbooks%2Froles%2Frestart_module) -> adapt to run on remote server
- [send_mail](playbooks%2Froles%2Fsend_mail) -> adapt to correctly send the mail
- [update_npa_file](playbooks%2Froles%2Fupdate_npa_file) -> everything ! 
  - Need to get the .profile
  - parse it to match its values to the NPA
  - decode its values using the right jasypt encoding
  - compare it to those of the NPA
  - if there is a change between cyberark and .profile for any NPA
    - backup .profile on remote server
    - rewrite it with the correct new values