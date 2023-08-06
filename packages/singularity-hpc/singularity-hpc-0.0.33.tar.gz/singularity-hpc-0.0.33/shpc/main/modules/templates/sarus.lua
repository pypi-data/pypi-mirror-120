-- Lmod Module
-- Created by singularity-hpc (https://github.com/singularityhub/singularity-hpc)
-- ##
-- {{ name }} on {{ creation_date }}
--

help(
[[
This module is a sarus container wrapper for {{ name }} v{{ version }}
{% if description %}{{ description }}{% endif %}

Container:

 - {{ image }}

Commands include:

 - {|module_name|}-run:
       {{ command }} run --tty {% if bindpaths %}--mount {{ bindpaths }} {% endif %}--mount ${PWD} --workdir ${PWD} <container> "$@"
 - {|module_name|}-shell:
       {{ command }} run --tty {% if bindpaths %}--mount {{ bindpaths }} {% endif %}--entrypoint {{ shell }} --mount ${PWD} --workdir ${PWD}<container>
 - {|module_name|}-exec:
       {{ command }} run --tty --entrypoint "" {% if bindpaths %}--mount {{ bindpaths }} {% endif %} --mount ${PWD} --workdir ${PWD} <container> "$@"

{% if aliases %}{% for alias in aliases %} - {{ alias.name }}:
       {{ command }} run --tty --entrypoint {{ alias.entrypoint }} {% if bindpaths %}--mount {{ bindpaths }} {% endif %}{% if alias.options %}{{ alias.options }} {% endif %} --mount ${PWD} --workdir ${PWD} <container> "{{ alias.args }}"
{% endfor %}{% endif %}

For each of the above, you can export:

 - SARUS_OPTS: to define custom options for {{ command }}
 - SARUS_COMMAND_OPTS: to define custom options for the command
]]) 

{% if sarus_module %}load("{{ sarus_module }}"){% endif %}
setenv ("SARUS_OPTS", "")
setenv ("SARUS_COMMAND_OPTS", "")

-- we probably don't need this
local MODULEPATH="{{ module_dir }}"

-- interactive shell to any container, plus exec for aliases
local containerPath = '{{ image }}'

local shellCmd = "sarus ${SARUS_OPTS} run --tty ${SARUS_COMMAND_OPTS} --entrypoint {{ shell }} {% if bindpaths %}--mount {{ bindpaths }} {% endif %} --mount ${PWD} --workdir ${PWD} " .. containerPath

-- execCmd needs entrypoint to be the executor
local execCmd = "sarus ${SARUS_OPTS} run ${SARUS_COMMAND_OPTS} --tty {% if bindpaths %}--mount {{ bindpaths }} {% endif %} --mount ${PWD} --workdir ${PWD} "
local runCmd = "sarus ${SARUS_OPTS} run ${SARUS_COMMAND_OPTS} --tty {% if bindpaths %}--mount {{ bindpaths }} {% endif %} --mount ${PWD} --workdir ${PWD} " .. containerPath

-- set_shell_function takes bashStr and cshStr
set_shell_function("{|module_name|}-shell", shellCmd,  shellCmd)

-- conflict with modules with the same name
conflict(myModuleName(){% if aliases %}{% for alias in aliases %}{% if alias.name != name %},"{{ alias.name }}"{% endif %}{% endfor %}{% endif %})

-- exec functions to provide "alias" to module commands
{% if aliases %}{% for alias in aliases %}
set_shell_function("{{ alias.name }}", execCmd .. {% if alias.options %} "{{ alias.options }} " .. {% endif %} " --entrypoint {{ alias.entrypoint }} " .. containerPath .. " {{ alias.args }} $@", execCmd .. {% if alias.options %} "{{ alias.options }} " .. {% endif %} " --entrypoint {{ alias.entrypoint }} " .. containerPath .. " {{ alias.args }}")
{% endfor %}{% endif %}

{% if aliases %}
if (myShellName() == "bash") then
{% for alias in aliases %}execute{cmd="export -f {{ alias.name }}", modeA={"load"}}
{% endfor %}
end{% endif %}

-- A customizable exec function
set_shell_function("{|module_name|}-exec", execCmd .. " --entrypoint \"\" " .. containerPath .. " $@",  execCmd .. " --entrypoint \"\" " .. containerPath)

-- Always provide a container run
set_shell_function("{|module_name|}-run", runCmd .. " $@",  runCmd)

whatis("Name        : " .. myModuleName())
whatis("Version     : " .. myModuleVersion())
{% if description %}whatis("Description    : {{ description }}"){% endif %}
{% if url %}whatis("Url         : {{ url }}"){% endif %}
{% if labels %}{% for key, value in labels.items() %}whatis("{{ key }}    : {{ value }}")
{% endfor %}{% endif %}
