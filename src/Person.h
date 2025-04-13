#pragma once
#include <ctime>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <random>

int GetRandomInt(int min, int max);
void GetVectorFromFile(const std::string& filename, std::vector<std::string>& names);

class Person {

public:
	static int id_generate;
	int count_povtor_visit;
	void SetId();
	void PrintPerson(std::ofstream& fout);
	void Generate_fio(const std::vector<std::string>& male_names, const std::vector<std::string>& female_names,
						const std::vector<std::string>& male_surnames, const std::vector<std::string>& female_surnames,
						const std::vector<std::string>& male_midnames, const std::vector<std::string>& female_midnames);
	void Generate_passport();
	void Generate_snils();
	void Generate_doctor_symp_an(const std::vector<std::string>& doctors_vector,
		const std::vector<std::string>& symptoms_vector,
		const std::vector<std::string>& analyzes_vector);
	void Generate_date_vis_and_an();
	void Generate_new_vis_and_an();
	void Generate_price();
	void Generate_card(int& x1, int& x2);
	void Generate_Person(std::vector<std::string>& male_names_vector,
		std::vector<std::string>& male_surnames_vector,
		std::vector<std::string>& male_midnames_vector,
		std::vector<std::string>& female_names_vector,
		std::vector<std::string>& female_surnames_vector,
		std::vector<std::string>& female_midnames_vector,
		std::vector<std::string>& symptoms_vector,
		std::vector<std::string>& doctors_vector,
		std::vector<std::string>& analyzes_vector, int& x1, int& x2);
	void Repeat_Person(std::vector<Person>& clinic, int& n,
		std::vector<std::string>& symptoms_vector,
		std::vector<std::string>& doctors_vector,
		std::vector<std::string>& analyzes_vector, int& x1, int& x2);

private:
	std::string id;
	struct tm timeStruct_vis = { 0 };
	struct tm timeStruct_an = { 0 };
	std::string fio;
	std::string passport;
	std::string snils;
	std::string symptoms;
	std::string doctor;
	std::string analyzes;
	std::string price;
	std::string card;
};