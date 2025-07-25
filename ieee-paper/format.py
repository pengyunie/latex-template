import sys


def format_tex(s: str, rec: bool = False, squeeze_lines: bool = False):
    output = ""
    formatted_lines = [""]
    for line in s.split("\n"):
        line = line.strip()
        # remove comment
        if len(line) > 0 and line[0] == "%":
            continue  # skip pure comment line

        line_wo_comment = ""
        parts = line.split("%")
        for pi, part in enumerate(parts):
            line_wo_comment += part
            if pi != len(parts) - 1:
                line_wo_comment += "%"
            if len(part) == 0 or part[-1] != "\\":
                # This is really a comment
                break
        line = line_wo_comment

        # embed \input
        if line[0:6] == "\\input":
            file_inputed = line[7:].split("}")[0]
            file_included = (
                file_inputed if file_inputed.endswith(".tex") else file_inputed + ".tex"
            )
            if file_included.startswith("tables/numbers-"):
                # Don't embed numbers files
                pass
            else:
                with open(file_included, "r") as f:
                    input_included = f.read()
                print(f"formatting {file_included}")
                line = format_tex(input_included, rec=True, squeeze_lines=False)

        # embed \lstinputlisting
        keyword = "\\lstinputlisting"
        if line.startswith(keyword):
            file_inputed = line[line.index("{") + 1 :].split("}")[0]
            file_included = (
                file_inputed if "." in file_inputed else file_inputed + ".tex"
            )
            with open(file_included, "r") as f:
                input_included = f.read()
            print(f"formatting {file_included}")
            listing_option = line[line.index("[") + 1 : line.index("]")]
            line = "\\begin{lstlisting}[" + listing_option + "]\n"
            line += input_included
            if not input_included.endswith("\n"):
                line += "\n"
            line += "\\end{lstlisting}"

        if squeeze_lines:
            # Minimize the number of line breaks
            if len(line.strip()) == 0:
                if (
                    len(formatted_lines) >= 2
                    and len(formatted_lines[-1].strip())
                    == len(formatted_lines[-2].strip())
                    == 0
                ):
                    # Put no more empty line
                    pass
                else:
                    # Put an empty line
                    formatted_lines.append("")
                    formatted_lines.append("")
            else:
                if len(formatted_lines[-1]) > 0:
                    formatted_lines[-1] += " "
                formatted_lines[-1] += line
                if line.strip()[-1] == "%" or len(formatted_lines[-1]) > 10000:
                    # Start a new line
                    formatted_lines.append("")
        else:
            formatted_lines.append(line)

    output = "".join([l + "\n" for l in formatted_lines])

    if rec is False:
        # remove \XComment \XSpace
        comment_words = ["XComment", "XSpace"]
        print(f"removing {comment_words}")

        for matchcmd in comment_words:
            matchstr = "\\" + matchcmd + "{"
            i = 0
            while i < len(output):
                if (
                    output[i : i + 1] == "\\"
                    and output[i : i + len(matchstr)] == matchstr
                ):
                    beg = i
                    depth = 1
                    j = i + len(matchstr)
                    while j < len(output):
                        if output[j : j + 1] == "{":
                            depth += 1
                        elif output[j : j + 1] == "}":
                            depth -= 1
                            if depth == 0:
                                break
                        j += 1

                    end = j + 1

                    if output[beg - 1] == "\n" and output[end] == "\n":
                        end = end + 1  # do not leave a blank line because of removing
                    output = output[0:beg] + output[end:]
                    if depth > 0:
                        print(
                            f"Warning: unexpected EOF. remaining unmatched bracket {depth}"
                        )
                else:
                    i += 1

    return output


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "main.tex"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "formatted.tex"
    with open(input_file, "r") as f:
        output = format_tex(f.read())

    with open(output_file, "w") as f:
        f.write(output)
