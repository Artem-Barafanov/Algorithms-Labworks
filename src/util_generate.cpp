#include <fstream>
#include <vector>
#include <string>
#include <iostream>

int GetRandomInt(int min, int max);

void util_1_generate(const std::string& filename) {
	std::ifstream file(filename);
	std::vector<std::string> vec;
	if (!file) {
		std::cout << "Error" << std::endl;
	}
	else {
		std::string line;
		while (std::getline(file, line)) {
			vec.push_back(line);
		}
	}
	file.close();

	std::ofstream fout(filename, std::ios_base::app);
	while (vec.size() > 0) {
		int i = GetRandomInt(0, vec.size() - 1);
		if (vec.size() >= 10) {
			for (int j = 0; j < 10; ++j) {
				int comb;
				do {
					comb = GetRandomInt(0, vec.size() - 1);
					if (i != comb) {
						fout << vec[i] << '/' << vec[comb] << std::endl;
					}
				} while (comb == i);
			}
		}
		else {
			for (int j = 0; j < vec.size(); ++j) {
				if (i != j) {
					fout << vec[i] << '/' << vec[j] << std::endl;
				}
			}
		}
		vec.erase(vec.begin() + i);
	}
	fout.close();
}

void util_2_generate() {
	std::ifstream file("symptoms_1.txt");
	std::vector<std::string> symptoms_1_vector;
	if (!file) {
		std::cout << "Error";
	}
	std::string line;
	int number = 0;
	while (!file.eof()) {
		std::getline(file, line);
		int counter = 1;
		number += 1;
		symptoms_1_vector.push_back((line));
		while (counter < 7) {
			std::getline(file, line);
			symptoms_1_vector.push_back((line));
			counter += 1;
			number += 1;
		}
		for (int i = number - 7; i < number - 1; ++i) {
			for (int j = i + 1; j < number; ++j) {
				symptoms_1_vector.push_back(symptoms_1_vector[i] + "/" + symptoms_1_vector[j]);
			}
		}

		for (int i = number - 7; i < number - 2; ++i) {
			for (int j = i + 1; j < number - 1; ++j) {
				for (int k = j + 1; k < number; ++k) {
					symptoms_1_vector.push_back(symptoms_1_vector[i] + "/" + symptoms_1_vector[j] + "/" + symptoms_1_vector[k]);
				}
			}
		}
		number += (21 + 35);
	}
	file.close();
	std::ofstream fout("symptoms.txt");
	for (int i = 0; i < symptoms_1_vector.size() - 1; ++i) {
		fout << symptoms_1_vector[i] << std::endl;
	}
	fout.close();
}