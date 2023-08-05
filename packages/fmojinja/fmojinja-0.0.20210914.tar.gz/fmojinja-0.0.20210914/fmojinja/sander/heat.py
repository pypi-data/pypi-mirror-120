from ..mixin import SanderMixin
from ..__version__ import get_version
from argparse import ArgumentParser


class Heating(SanderMixin):
    """
    e.g. python -m fmojinja.sander heat > $*.in; sander -O -i $*.in -o $*.mdout -r $*.rst_opt -p $*.parm -c $< -ref $<
    """

    @classmethod
    def template(cls):
        return "{{ title }}" + f" !Generated by fmojinja version {get_version()}" + """ 
&cntrl
  nmropt={{ nmropt }},
  ntx={{ inpcrd_option }},
  irest={{ restart }},
""" + cls.write_general_jinja() + """
  tempi={{ temperature_init }},
  iwrap={{ iwrap }},
/
{%- if nmropt > 0 %}
&wt 
  type='TEMP0', 
  istep1=0, 
  istep2={{ (nsteps_limit * 0.8) | int }}, 
  value1={{ temperature_init }}, 
  value2={{ temperature }}, 
/
&wt 
  type='END', 
/
{%- endif %}

"""

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p = super(Heating, cls).set_arguments(p)
        p.add_argument("-nmropt", default=1)
        p.add_argument("-ntx", "--inpcrd-option", type=int, default=1)
        p.add_argument("-irest", "--restart", type=int, default=0)
        p.add_argument("-tempi", "--temperature-init", default=0)
        return p
