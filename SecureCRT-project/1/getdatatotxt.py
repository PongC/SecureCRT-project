file = open("commands.txt").read().split("\n")
file=list(filter(('').__ne__, file))
print(file)
