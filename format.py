import sys


def format_tex(s: str, rec: bool = False, squeeze_lines: bool = False):
    output = ""
    formatted_lines = [""]
    for line in s.split("\n"):
        # remove comment
        if len(line) > 0 and line[0] == "%":  continue  # skip pure comment line

        line_wo_comment = ""
        parts = line.split("%")
        for pi, part in enumerate(parts):
            line_wo_comment += part
            if pi != len(parts)-1:
                line_wo_comment += "%"
            # end if
            if len(part) == 0 or part[-1] != "\\":
                # This is really a comment
                break
            # end if
        # end for
        line = line_wo_comment

        # embed \input
        if line[0:6] == "\\input":
            file_inputed = line[7:].split("}")[0]
            file_included = file_inputed if file_inputed.endswith(".tex") else file_inputed + ".tex"
            if file_included.startswith("tables/numbers-"):
                # Don't embed numbers files
                pass
            else:
                with open(file_included, "r") as f:
                    input_included = f.read()
                # end with
                print(f"formatting {file_included}")
                line = format_tex(input_included,
                                  rec=True,
                                  squeeze_lines=False)
            # end if
        # end if

        if squeeze_lines:
            # Minimize the number of line breaks
            if len(line.strip()) == 0:
                if len(formatted_lines) >= 2 and len(formatted_lines[-1].strip()) == len(formatted_lines[-2].strip()) == 0:
                    # Put no more empty line
                    pass
                else:
                    # Put an empty line
                    formatted_lines.append("")
                    formatted_lines.append("")
                # end if
            else:
                if len(formatted_lines[-1]) > 0:  formatted_lines[-1] += " "
                formatted_lines[-1] += line
                if line.strip()[-1] == "%" or len(formatted_lines[-1]) > 10000:
                    # Start a new line
                    formatted_lines.append("")
                # end if
            # end if
        else:
            formatted_lines.append(line)
        # end if
    # end for

    output = "".join([l+"\n" for l in formatted_lines])

    if rec == False:
        # remove \XComment \XSpace
        comment_words = ["XComment", "XSpace"]
        print(f"removing {comment_words}")

        for matchcmd in comment_words:
            matchstr = "\\" + matchcmd + "{"
            i = 0
            while i < len(output):
                if output[i:i+1] == "\\" and output[i:i+len(matchstr)] == matchstr:
                    beg = i
                    depth = 1
                    j = i + len(matchstr)
                    while j < len(output):
                        if output[j:j+1] == "{":
                            depth += 1
                        elif output[j:j+1] == "}":
                            depth -= 1
                            if depth == 0:
                                break
                            # end if
                        # end if
                        j += 1
                    # end while
                                        
                    end = j + 1

                    if output[beg - 1] == '\n' and output[end] == '\n':
                        end = end + 1 # do not leave a blank line because of removing
                    # end if
                    output= output[0:beg] + output[end:]
                    if depth > 0:
                        print(f"Warning: unexpected EOF. remaining unmatched bracket {depth}")
                    # end if
                else:
                    i += 1
                # end if
            # end while
        # end for
    # end if

    return output


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "main.tex"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "formatted.tex"
    with open(input_file, "r") as f:
        output = format_tex(f.read())
    # end with

    with open(output_file, "w") as f:
        f.write(output)
    # end with
# end if
