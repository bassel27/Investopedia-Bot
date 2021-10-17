def returnOrdinal(number):
	ordinalDict = {
		1: "First",
		2: "Second",
		3: "Third",
		4: "Fourth",
		5: "Fifth",
		6: "Sixth",
		7: "Seventh",
		8: "Eighth",
		9: "Ninth",
		10: "Tenth",
		11: "Eleventh",
		12: "Twelfth",
		13: "Thirteenth",
		14: "Fourteenth",
		15: "Fifteenth",
	}
	
	return ordinalDict.get(number, "nothing")