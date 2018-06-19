match_file <- read.csv(file="Data/CNF-FNDDS.matches.csv", head=TRUE, sep=",")

exact_match <- 0
no_match <- 0

get_raw_number <- function(str) {
  str = strsplit(str, ";")
  str = str[[1]][1]
  str = strsplit(str, "match")
  str = str[[1]][1]
  str = strsplit(str, "\\(")
  str = str[[1]][length(str[[1]])]
  str = strsplit(str, "%")
  str = str[[1]][1]
  if (is.na(str)) str = 0
  return(as.numeric(str))
}

for (match in match_file$US.Matches) {
  match = get_raw_number(match)
  
  if(match > 95) {
    exact_match = exact_match + 1
  } else if(match == 0) {
    no_match = no_match + 1
  }
}

no_match = no_match/nrow(match_file)*100
exact_match = exact_match/nrow(match_file)*100

H <- c(no_match, exact_match)
names <- c("No Match", "Exact Match")


barplot(H, ylab = "Percentage of dataset (%)", names.arg=names , main="CNF-FNDDS results")
text(.75, 50, round(no_match, 2))
text(1.75, 5, round(exact_match, 2))



