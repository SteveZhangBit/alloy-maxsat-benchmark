abstract sig Person {
	tags: set Tag
}
one sig P1, P2, P3, P4, P5 extends Person {}

abstract sig Tag {}
one sig A, B, C extends Tag {}

fact {
	tags = P1 -> A + P1 -> B +
		P2 -> C +
		P3 -> B +
		P4 -> C + P4 -> A +
		P5 -> A
} 

sig Table {
	seat: set Person,
} {
	#seat < 4
	#seat > 1
}

fact {
	all p: Person | one seat.p
}

run {
	// table-based
	all t: Table | minsome t.seat.tags and
		// additional semantics for a tag is not in a table
		all tag: Tag | tag !in t.seat.tags implies
			no p: Person | t -> p in seat and p -> tag in tags
} for 2 Table

run {
	// tag-based
	all t: Tag | minsome seat.tags.t and
		all tab: Table | tab !in seat.tags.t implies
			no p: Person | tab -> p in seat and p -> t in tags
} for 2 Table
