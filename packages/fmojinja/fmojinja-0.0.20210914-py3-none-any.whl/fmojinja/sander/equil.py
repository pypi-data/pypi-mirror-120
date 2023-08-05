from ..mixin import SanderMixin
from ..__version__ import get_version
from argparse import ArgumentParser


class Equilibration(SanderMixin):
    """
    e.g. python -m fmojinja.sander heat > $*.in; sander -O -i $*.in -o $*.mdout -r $*.rst_opt -p $*.parm -c $< -ref $<
    """

    @classmethod
    def template(cls):
        return "{{ title }}" + f" !Generated by fmojinja version {get_version()}" + """ 
&cntrl
  ntx={{ inpcrd_option }},
  irest={{ restart }},
""" + cls.write_general_jinja() + """
  ntp={{ pressure_regulation }},
/

"""

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p = super(Equilibration, cls).set_arguments(p)
        p.add_argument("-ntx", "--inpcrd-option", type=int, default=5)
        p.add_argument("-irest", "--restart", type=int, default=1)
        p.add_argument("-ntp", "--pressure-regulation", default=1)
        return p
