# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 09:59:23 2018

@author: jenkinscc
"""
import os


def open_Diag_file(diagnostic_file):
    with open(diagnostic_file, 'r') as c:
        Diag_ions = {}
        line = c.readlines()
        for item in line[0:-1]:
            remove_newline = item.strip()
            x = remove_newline.split(':')
            Diag_ions[x[0]] = x[1]
        return Diag_ions


def open_glyco(glyco_file):
    with open(glyco_file, 'r') as g:
        glyco_reporters = []
        line = g.readlines()
        for item in line:
            clean_item = item.strip()
            glyco_reporters.append(clean_item)
        return glyco_reporters


def separate_scan_csv(name):
    with open(name, 'r') as file:
        x = file.read().split('BEGIN IONS')
        return x[1:]


# working_directory = os.getcwd()


def run(working_directory, diag_ions_file: str, glyco_repoters_file: str, tolerance, min_feature_counter: int):
    file_list = []

    for root, dirs, files in os.walk(working_directory):
        for name in files:
            if name.endswith('.mgf'):
                file_list.append(os.path.join(root, name))
            else:
                pass
    file_list.sort()
    # M/Z Tolerance below here
    # tolerance = 0.005

    Diag_ions = open_Diag_file(diag_ions_file)
    glyco_ions = open_glyco(glyco_repoters_file)

    for name in file_list:
        file_directory = os.path.dirname(name)
        new_file_name = "Filtered_" + os.path.join(os.path.basename(name))
        new_file_path = os.path.join(os.path.dirname(name), new_file_name)

        with open(new_file_path, 'w') as f:  # Opens up a new filtered file to write to
            f.writelines('MASS=Monoisotopic' + '\n')
            count_Dict = {}
            glyco_count = 0
            for key, value in Diag_ions.items():
                count_Dict[key] = 0
            for MS1 in separate_scan_csv(name):
                feature_counter = 0
                clean_MS1 = MS1.strip()  # removes the whitespaces in the scan
                entry = clean_MS1.split('\n')  # scan is made up of header and ions sp this splits them
                header = entry[0:5]
                scans = entry[5:-1]
                scanstring = '\n'.join(
                    scans)  # Since each ion is separated by a new line, we want to remove the new line
                scan_list = [i.split(' ') for i in
                             scans]  # the removal of the new line enables us to split the ions seen in the scan
                for m_z in scan_list:  # this part calculates the min a max of the mass of the observed reporter ions
                    reading = float(m_z[0])
                    lower = float(reading) - tolerance
                    upper = float(reading) + tolerance
                    for key, value in Diag_ions.items():
                        if lower <= float(value) <= upper:
                            count_Dict[key] += 1
                            feature_counter += 1
                    for item in glyco_ions:
                        if lower <= float(item) <= upper:
                            glyco_count += 1
                            feature_counter += 1
                # Change feature counter if you want multiple DIs
                if feature_counter >= min_feature_counter:
                    print('Writing Spectra ', header[0])
                    f.writelines('BEGIN IONS' + '\n')
                    f.writelines(header[0] + '\n')
                    f.writelines(header[1] + '\n')
                    f.writelines(header[2] + '\n')
                    f.writelines(header[3] + '\n')
                    f.writelines(header[4] + '\n')
                    f.writelines(scanstring)
                    f.writelines('\n')
                    f.writelines('END IONS' + '\n' + '\n')

        diagnostic_file_path = os.path.join(file_directory, f"Diagnostic_{new_file_name}")
        with open(diagnostic_file_path, 'w') as f:
            for key, value in count_Dict.items():
                f.writelines(key + ':' + str(value) + '\n')
            f.writelines('Glyco:' + str(glyco_count))

        return "Completed!"
