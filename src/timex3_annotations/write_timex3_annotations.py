#
# This file is part of QTCR-VERIFICATOR.
#
# QTCR-VERIFICATOR is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# QTCR-VERIFICATOR is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with QTCR-VERIFICATOR (file COPYING in the main directory). If not, see
# http://www.gnu.org/licenses/.

import os
import helpers


def main():
    files = os.listdir(helpers.process_description_path)
    for file in files:
        if os.path.isfile(os.path.join(helpers.process_description_path, file)):
            f = open(os.path.join(helpers.process_description_path, file), 'r')
            helpers.create_annotated_file(helpers.timex3_annotations_path + file[:-4] + '.xml', helpers.get_temporally_annotated_text(
                helpers.get_all_sentences(f)))
            f.close()


if __name__ == '__main__':
    main()