// Implement the 'wc' unix tool which stands for 'word count'. It can count number of lines,
// words and characters and this is my Python implementation of the same
// This coding challenge can be found at: https://codingchallenges.fyi/challenges/challenge-wc

package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// Helper function

func printResults(getOutput []string) error {

	if len(getOutput) <= 0 {
		return fmt.Errorf("Error in printing results")
	}

	for _, output := range getOutput {
		fmt.Println(output)
	}

	return nil

}

func getBytes(filePaths []string) ([]string, error) {
	
	var results []string
	totalBytes := int64(0)

	for _, path := range filePaths {
		file, err := os.Open(path)
		if err != nil {
			return nil, err
		}
		defer file.Close()

		// Get file statistics
		fileInfo, err := file.Stat()
		if err != nil {
			return nil, err
		}

		// Size of the file
		fileSize := fileInfo.Size()
		results = append(results, fmt.Sprintf("%d %s", fileSize, path))
		totalBytes += fileSize
	}

	if len(filePaths) == 1 {
		return results, nil
	}

	results = append(results, fmt.Sprintf("%d total", totalBytes))
	return results, nil

}

func getLines(filePaths []string) ([]string, error) {

	var results []string
	totalLines := 0

	for _, path := range filePaths {
		file, err := os.Open(path)
		if err != nil {
			return nil, err
		}
		defer file.Close()

		scanner := bufio.NewScanner(file)
		lineCount := 0
		for scanner.Scan() {
			lineCount += 1
		}
		if err := scanner.Err(); err != nil {
			return nil, err
		}

		results = append(results, fmt.Sprintf("%d %s", lineCount, path))
		totalLines += lineCount
	}

	if len(filePaths) == 1 {
		return results, nil
	}

	results = append(results, fmt.Sprintf("%d total", totalLines))
	return results, nil

}

func getWords(filePaths []string) ([]string, error) {

	var results []string
	totalWords := 0

	for _, path := range filePaths {
		file, err := os.Open(path)
		if err != nil {
			return nil, err
		}
		defer file.Close()

		scanner := bufio.NewScanner(file)
		wordCount := 0
		for scanner.Scan() {
			wordCount += len(strings.Fields(scanner.Text()))
		}
		if err = scanner.Err(); err != nil {
			return nil, err
		}

		results = append(results, fmt.Sprintf("%d %s", wordCount, path))
		totalWords += wordCount
	}

	if len(filePaths) == 1 {
		return results, nil
	}

	results = append(results, fmt.Sprintf("%d total", totalWords))
	return results, nil

}

func getCharacters(filePaths []string) ([]string, error) {

	var results []string
	totalCharacters := 0

	for _, path := range filePaths {
		file, err := os.Open(path)
		if err != nil {
			return nil, err
		}
		defer file.Close()

		scanner := bufio.NewScanner(file)
		characterCount := 0
		for scanner.Scan() {
			characterCount += len(scanner.Text())
		}
		if err = scanner.Err(); err != nil {
			return nil, err
		}

		results = append(results, fmt.Sprintf("%d %s", characterCount, path))
		totalCharacters += characterCount
	}

	if len(filePaths) == 1 {
		return results, nil
	}

	results = append(results, fmt.Sprintf("%d total", totalCharacters))
	return results, nil

}

func getAll(filePaths []string) ([]string, error) {

	var results []string
	totalCount := []int{0, 0, 0}

	for _, path := range filePaths {
		file, err := os.Open(path)
		if err != nil {
			return nil, err
		}
		defer file.Close()

		linesResult, err := getLines([]string{path})
		if err != nil {
			return nil, err
		}
		linesCount, err := strconv.Atoi(strings.Fields(linesResult[0])[0])
		if err != nil {
			return nil, err
		}

		wordsResult, err := getWords([]string{path})
		if err != nil {
			return nil, err
		}
		wordsCount, err := strconv.Atoi(strings.Fields(wordsResult[0])[0])
		if err != nil {
			return nil, err
		}

		bytesResponse, err := getBytes([]string{path})
		if err != nil {
			return nil, err
		}
		bytesCount, err := strconv.Atoi(strings.Fields(bytesResponse[0])[0])
		if err != nil {
			return nil, err
		}

		results = append(results, fmt.Sprintf("%d %d %d %s", linesCount, wordsCount, bytesCount, path))
		addTotal := []int{linesCount, wordsCount, bytesCount}
		for i := 0; i < 3; i++ {
			totalCount[i] += addTotal[i]
		}
	}

	if len(filePaths) == 1 {
		return results, nil
	}

	results = append(results, fmt.Sprintf("%d %d %d total", totalCount[0], totalCount[1], totalCount[2]))
	return results, nil

}

func getResults(option string, filePaths []string, defaultGetAllFlag bool, nonDirectCommand bool) error {

	if defaultGetAllFlag == true {
		getOutput, err := getAll(filePaths)
		if err != nil {
			return fmt.Errorf("Error getting all options %v", err)
		}

		if err = printResults(getOutput); err != nil {
			return fmt.Errorf("Error printing results %v", err)
		}

		return nil
	}

	if option == "-c" {
		if nonDirectCommand == false {
			filePaths = filePaths[1:]
		}
		getOutput, err := getBytes(filePaths)
		if err != nil {
			return fmt.Errorf("Error getting bytes in -c option %v", err)
		}

		if err = printResults(getOutput); err != nil {
			return fmt.Errorf("Error printing results %v", err)
		}
	} else if option == "-l" {
		if nonDirectCommand == false {
			filePaths = filePaths[1:]
		}
		getOutput, err := getLines(filePaths)
		if err != nil {
			return fmt.Errorf("Error getting lines in -l option %v", err)
		}
 
		if err = printResults(getOutput); err != nil {
			return fmt.Errorf("Error printing results %v", err)
		}
	} else if option == "-w" {
		if nonDirectCommand == false {
			filePaths = filePaths[1:]
		}
		getOutput, err := getWords(filePaths)
		if err != nil {
			return fmt.Errorf("Error getting words in -m option %v", err)
		}

		if err = printResults(getOutput); err != nil {
			return fmt.Errorf("Error printing results %v", err)
		}
	} else if option == "-m" {
		if nonDirectCommand == false {
			filePaths = filePaths[1:]
		}
		getOutput, err := getCharacters(filePaths)
		if err != nil {
			return fmt.Errorf("Error getting characters in -m option %v", err)
		}

		if err = printResults(getOutput); err != nil {
			return fmt.Errorf("Error printing results %v", err)
		}
	} else if strings.HasPrefix(option, "-") {
		return fmt.Errorf("Incorrect option")
	} else {
		getOutput, err := getAll(filePaths)
		if err != nil {
			return fmt.Errorf("Error getting all options %v", err)
		}

		if err = printResults(getOutput); err != nil {
			return fmt.Errorf("Error printing results %v", err)
		}
	}

	return nil
}

func main() {

	scanner := bufio.NewScanner(os.Stdin)

	// Take CLI input

	fmt.Printf("> ")

	scanner.Scan()
	cliInput := scanner.Text()

	if err := scanner.Err(); err != nil {
		fmt.Println("Error reading input: ", err)
		return
	}

	// Check if command starts with 'ccwc' or not
	if strings.HasPrefix(cliInput, "ccwc") {

		cliArgs := strings.Fields(cliInput)

		if len(cliArgs) < 2 {
			fmt.Println("Not enough arguments passed")
			return
		}

		option := cliArgs[1]
		if err := getResults(option, cliArgs[1:], false, false); err != nil {
			fmt.Println("Error getting results in ccwc command: ", err)
			return
		}

	} else {

		cliArgs := strings.Split(cliInput, "|")

		if len(cliArgs) < 2 {
			fmt.Println("Not enough arguments")
			return
		}

		checkFilePos := 1
		for i := 1; i < len(cliArgs); i++ {
			if strings.HasPrefix(strings.TrimSpace(cliArgs[i]), "ccwc") {
				checkFilePos = i - 1
				break
			}
		}

		filesPath := strings.Fields(cliArgs[checkFilePos])[1:]

		option := strings.Fields(cliArgs[checkFilePos + 1])

		if len(option) == 1 {
			if err := getResults(option[0], filesPath, true, true); err != nil {
				fmt.Println("Error in getting all options results: ", err)
				return
			}
		} else {
			if err := getResults(option[1], filesPath, false, true); err != nil {
				fmt.Println("Error in getting results: ", err)
				return
			}
		}
	}
}
