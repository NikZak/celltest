"""Cell functions."""
from collections import defaultdict
from tokenize import (untokenize, NEWLINE, NAME, OP)
import re
import shlex
import os
import nbformat
import celltest
from celltest.utils import (glue, _tokenize, indent, replace_asserts,
                            save_outputs, remove_docstring,
                            get_template_from_file, get_notebook_name,
                            get_template_file, logger, root_logger,
                            parse_params)
from celltest.funclib import get_outputs


class CellConvert():
  """Notebook convert."""

  def __init__(self, **kwargs):
    """Read all relevant info from notebook."""
    # default values
    default_kwargs = {
        "filepath": None,
        "callbacks": [],
        "insert_saved_outputs": True,
        "output_file": None,
        "header_file": None,
        "standard_template": None,
        "custom_template": None,
        "verbose": False,
    }
    self.accepted = {
        "params": [
            "comment", "setup", "ignore_outputs", "ignore_stderr",
            "ignore_stdout", "ignore", "ignore_display_data", "run_all_till_now"
        ],
        "callbacks": [("black",), ("yapf", "-i"), ("isort",)]
    }

    # check params
    for kwarg in kwargs:
      if kwarg not in default_kwargs:
        raise ValueError("Unknown parameter: %s" % kwarg)
    self.kwargs = default_kwargs.copy()
    self.kwargs.update(kwargs)
    for callback in self.kwargs["callbacks"]:
      if callback not in [x[0] for x in self.accepted["callbacks"]]:
        raise ValueError("Unknown callback: %s" % callback)

    if self.kwargs["verbose"]:
      logger.setLevel('DEBUG')
    else:
      logger.setLevel(root_logger.handlers[0].level)

    # get input filepath. If not provided assuming we're in notebook environment
    # and current file is the one to be transformed
    if self.kwargs["filepath"] is None:
      try:
        self.filepath = get_notebook_name()
      except Exception as excp:
        raise ValueError(
            "Notebook name not provided and could "
            "not be derived from current environment. Please "
            "provide notebook name(s) that has to be converted") from excp
    else:
      self.filepath = os.path.join(os.getcwd(), self.kwargs["filepath"])

    # read template
    template_file = get_template_file(self.kwargs["standard_template"],
                                      self.kwargs["custom_template"])
    self.templ = get_template_from_file(template_file)
    if not self.templ:
      raise ValueError("Could no read template from file %s" %
                       self.kwargs["template_file"])

    # gather header control params
    self.control_params_d = defaultdict(dict)
    for header_line in ["insert_saved_outputs", "header_file"]:
      if self.kwargs[header_line]:
        self.control_params_d["head_level"][header_line] = True

    # gather replacements for the template file
    self.replacements = {}  # defaultdict(lambda: None)
    with open(os.path.join(os.path.dirname(celltest.__file__),
                           "funclib.py")) as funclib_file:
      self.replacements["funclib"] = remove_docstring(funclib_file.read())
    if self.kwargs["header_file"]:
      with open(kwargs["header_file"]) as file_:
        self.replacements["header_file"] = file_.read()
    self.replacements["accepted_params"] = self.accepted["params"]
    self.replacements["accepted_callbacks"] = ", ".join(
        x[0] for x in self.accepted["callbacks"])
    self.replacements["filefullpath"] = self.filepath
    self.replacements["notebook_name"] = os.path.split(self.filepath)[1]

    # gather code, outputs, and metadata
    self.code_d_ = {}  # this will be changing
    self.metadata_d = {}
    self.ct_saved_cell_outputs = get_outputs(self.filepath, pretty_quotes=True)
    with open(self.filepath) as file:
      self.cells = nbformat.read(file, nbformat.NO_CONVERT).cells
      # for ease of usage read all relevant cells into separate lists
      for index, cell in enumerate(self.cells):
        if cell.cell_type == "code":
          self.code_d_[index] = cell.source
        if "celltest" in cell.metadata:
          self.metadata_d[index] = cell.metadata.celltest

    # get file name where to write the results
    path, name = os.path.split(self.filepath)
    name = os.path.splitext(name)[0]
    if self.kwargs["output_file"]:
      self.output = self.kwargs["output_file"]
    else:
      self.output = os.path.join(path, "test_" + name + ".py")

  def carve_magic(self, update=True):
    """Carve out notebook magic."""
    clean_code_d = {}
    magic_code_d_ = {}
    for cell_index, cell in self.code_d_.items():
      lines = cell.split("\n")
      if lines[0].strip().startswith("%"):
        magic_code_d_[cell_index] = lines[0]
        clean_code_d[cell_index] = "\n".join(lines[1:])
      else:
        clean_code_d[cell_index] = cell
    if update:
      self.code_d_ = clean_code_d
    return magic_code_d_, clean_code_d

  def carve_control_params(self, update=True):
    """Read control params from comments or metadata."""
    control_params_d = defaultdict(dict)
    clean_code_d = {}

    # params first get collected from metadata
    for cell_index, metadata in self.metadata_d.items():
      params_d = parse_params(metadata, self.accepted["params"])
      control_params_d[cell_index].update(params_d)

    # then from cell itself, if conflict cell params have priority
    for cell_index, cell in self.code_d_.items():
      lines = cell.split("\n")
      if lines[0].strip().startswith("%"):
        lines.pop(0)
      params_string = re.match(r"^#\s+CT:(.*)", lines[0].strip())
      if params_string:
        params_string_ = params_string[1]
        clean_code_d[cell_index] = "\n".join(lines[1:])
      else:
        params_string_ = ""
        clean_code_d[cell_index] = cell

      params_d = parse_params(
          shlex.split(params_string_), self.accepted["params"])
      control_params_d[cell_index].update(params_d)

    if update:
      self.code_d_ = clean_code_d

    self.control_params_d.update(control_params_d)
    return self.control_params_d

  def carve_setup(self, update=True):
    """Get setup code."""
    setup_code_l = []
    clean_code_d = {}
    for cell_index, cell in self.code_d_.items():
      if "setup" in self.control_params_d[cell_index]:
        setup_code_l.append(cell.strip())
      else:
        clean_code_d[cell_index] = cell
    setup_code = "\n".join(setup_code_l)

    logger.debug("setUp code: %s", setup_code)
    if update:
      self.code_d_ = clean_code_d
    self.replacements["setup"] = setup_code
    return setup_code, clean_code_d

  def remove_backslash(self, update=True):
    """Remove backslash at the end of the line."""
    # TODO(NikZak) for \ inside """ or inside a comment, redo with tokenizer
    clean_code_d = {}
    for index, cell in self.code_d_.items():
      if cell:
        cell_source = re.sub(r"\\\n\s*", " ", cell)
        clean_code_d[index] = cell_source
    if update:
      self.code_d_ = clean_code_d
    return clean_code_d

  def carve_imports(self, update=True):
    """Get imports code."""
    # assemble import code
    import_tokens = []
    clean_code_d_ = {}
    for cell_index, cell in self.code_d_.items():
      if "ignore" in self.control_params_d[cell_index]:
        continue

      # find imports
      tokens = [(x[0], x[1]) for x in _tokenize(cell)]
      logger.debug("Tokens: %s", tokens)
      tokens_clean = []
      start_import_line = None

      for index, token in enumerate(tokens):
        if start_import_line is not None:
          if token[0] == NEWLINE:
            import_tokens += tokens[start_import_line:index] + [(NEWLINE, '\n')]
            logger.debug("Added imports: %s",
                         tokens[start_import_line:index] + [(NEWLINE, '\n')])
            start_import_line = None
            continue
        else:
          if token[0] == NAME and (token[1] == "import" or token[1] == "from"):
            start_import_line = index
            logger.debug("Started import line: %d", start_import_line)
          else:
            tokens_clean.append(token)
      clean_code_d_[cell_index] = untokenize(tokens_clean)

    # add imports with no indentation
    import_code = untokenize(import_tokens)
    logger.debug("import_code: %s", import_code)

    # remove duplicates
    import_code_l = import_code.split("\n")
    import_code_l = list(dict.fromkeys(import_code_l))
    import_code = "\n".join(import_code_l)

    logger.debug("imports code: %s", import_code)

    if update:
      self.code_d_ = clean_code_d_
    self.replacements["imports"] = import_code
    return import_code, clean_code_d_

  def run(self):
    """Run in correct order."""
    self.remove_backslash()
    self.carve_magic()
    self.carve_control_params()
    self.carve_imports()
    self.carve_setup()
    self.make_tests()

  def apply_callbacks(self, output_string, callbacks):
    """Apply callbacks."""
    for callback in callbacks:
      if callback not in [x[0] for x in self.accepted["callbacks"]]:
        logger.error("Uknonwn callback %s", callback)
        continue
      if callback == "isort":
        import isort  # pylint: disable=import-outside-toplevel
        output_string = isort.code(output_string)  # pylint: disable=import-outside-toplevel
      if callback == "black":
        from black import format_str, FileMode  # pylint: disable=import-outside-toplevel
        output_string = format_str(output_string, mode=FileMode())
      if callback == "yapf":
        from yapf.yapflib.yapf_api import FormatCode  # pylint: disable=import-outside-toplevel
        from yapf.yapflib import file_resources  # pylint: disable=import-outside-toplevel
        style_config = file_resources.GetDefaultStyleForDir(os.getcwd())

        output_string = FormatCode(output_string, style_config=style_config)
        # yapf<0.3 returns diff as str, >=0.3 returns a tuple of (diff, changed)
        output_string = output_string[0] if isinstance(output_string,
                                                       tuple) else output_string
    return output_string

  def check_cells(self, index_iter):
    """Check that the cell code respects control params."""
    if "ignore" in self.control_params_d[index_iter]:
      return False
    ops = [x[0] for x in _tokenize(self.code_d_[index_iter])]
    if OP not in ops and NAME not in ops:
      #code should do at least something meaningful
      return False
    return True

  def check_cells_if(self, index_iter, control_line=None):
    """Check that the cell code respects control params."""
    if control_line is None:
      control_line = []
    for check in control_line:
      check_l = check.split(" ")
      if check_l[0] == "not" and len(check_l) > 1:
        check = " ".join(check_l[1:])
        if check not in self.accepted["params"]:
          logger.error("Unknown param: %s in template.py. Ignoring", check)
        if check in self.control_params_d[index_iter]:
          return False
      else:
        if check not in self.control_params_d[index_iter]:
          return False
    return True

  def check_head_if(self, control_line=None):
    """Check that the cell code respects control params."""
    if control_line is None:
      control_line = []
    for check in control_line:
      check_l = check.split(" ")
      if check_l[0] == "not" and len(check_l) > 1:
        check = " ".join(check_l[1:])
        if check in self.control_params_d["head_level"]:
          return False
      else:
        if check not in self.control_params_d["head_level"]:
          return False
    return True

  def make_tests_iter(self, templ_, output_string, cell_index=None):
    """Walk iteratively through the template."""
    for _, code_piece in sorted(templ_.items()):
      if "control" in code_piece:
        if "if_head_level" in code_piece["control"]:
          if not self.check_head_if(code_piece["control"]["if_head_level"]):
            continue
        if "if_cell_level" in code_piece["control"]:
          if cell_index and not self.check_cells_if(
              cell_index, code_piece["control"]["if_cell_level"]):
            continue
        if "loop" in code_piece["control"]:
          templ_piece = code_piece["source"]
          for index_iter, value_iter in self.__dict__[code_piece["control"]
                                                      ["loop"]].items():
            self.replacements["index_iter"] = index_iter
            self.replacements["index_iter_name"] = str(index_iter).zfill(5)
            self.replacements["value_iter"] = value_iter
            if "comment" in self.control_params_d[index_iter]:

              self.replacements["comment"] = self.control_params_d[index_iter][
                  "comment"].replace('"', '\\"')
            self.replacements[
                "ct_saved_cell_outputs_stdout"] = self.ct_saved_cell_outputs[
                    index_iter]["stdout"]
            self.replacements[
                "ct_saved_cell_outputs_stderr"] = self.ct_saved_cell_outputs[
                    index_iter]["stderr"]
            self.replacements[
                "ct_saved_cell_outputs_display_data"] = self.ct_saved_cell_outputs[
                    index_iter]["display_data"]
            self.replacements["run_all_till_now"] = (
                self.replacements["setup"] +
                "".join(value for key, value in self.code_d_.items()
                        if key < index_iter))

            if not self.check_cells(index_iter):
              continue
            output_string = self.make_tests_iter(
                templ_piece, output_string, cell_index=index_iter)
          continue

      code_formatted = code_piece["source"]

      if "replacements" in code_piece:
        replacements = [
            self.replacements[x] for x in code_piece["replacements"]
        ]
        code_formatted = code_formatted.format(*replacements)

      if "callbacks" in code_piece:
        for callback in code_piece["callbacks"]:
          if callback == "replace_asserts":
            code_formatted = replace_asserts(code_formatted)
          if callback == "save_outputs":
            code_formatted = save_outputs(code_formatted)

      if "indent" in code_piece:
        code_formatted = indent(code_formatted, count=code_piece["indent"])

      output_string = glue(output_string, code_formatted)

    return output_string

  def make_tests(self, update=True, callbacks=None, insert_saved_outputs=None):
    """Assemle test file."""
    if callbacks is None:
      callbacks = self.kwargs["callbacks"]
    if insert_saved_outputs is None:
      insert_saved_outputs = self.kwargs["insert_saved_outputs"]
    output_string = ""
    output_string = self.make_tests_iter(self.templ, output_string)

    if callbacks:
      output_string = self.apply_callbacks(output_string, callbacks)

    logger.debug(output_string)

    # Writing to file
    if update:
      with open(self.output, "w") as file1:
        file1.write(output_string)
    return output_string
