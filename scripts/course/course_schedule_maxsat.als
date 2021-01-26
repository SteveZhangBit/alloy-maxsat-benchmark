abstract sig Day {}
one sig Mon, Tue, Wed, Thu, Fri extends Day {}

abstract sig Time {}
one sig AM, PM extends Time {}

abstract sig Course {
	lectures: set Lecture
}
one sig CS101, Compiler, OS, ML, SE extends Course {}

fact {
	lectures = CS101 -> MonAM + CS101 -> WedAM + CS101 -> FriPM +
		ML -> TueAM + ML -> ThuAM +
		SE -> MonPM + SE -> WedPM +
		Compiler -> TueAM + Compiler -> ThuAM +
		OS -> TuePM + OS -> ThuPM
}

abstract sig Lecture {
	day: one Day,
	time: one Time
}
one sig MonAM, MonPM, TueAM, TuePM, WedAM, WedPM,
			  ThuAM, ThuPM, FriAM, FriPM extends Lecture {}

fact {
	day = MonAM -> Mon + MonPM -> Mon +
		TueAM -> Tue +TuePM -> Tue +
		WedAM -> Wed + WedPM -> Wed +
		ThuAM -> Thu + ThuPM -> Thu +
		FriAM -> Fri + FriPM -> Fri
	time = MonAM -> AM + MonPM -> PM +
		TueAM -> AM +TuePM -> PM +
		WedAM -> AM + WedPM -> PM +
		ThuAM -> AM + ThuPM -> PM +
		FriAM -> AM + FriPM -> PM
}

abstract sig Student {
	core: set Course,
	interests: set Course,
	courses: set Course
}
one sig Alice extends Student {} {
	core = CS101
	interests = ML + SE
}

pred conflict[c1, c2: Course] {
	some l1, l2: Lecture {
		l1 in c1.lectures
		l2 in c2.lectures
		l1.day = l2.day
		l1.time = l2.time
	}
}

pred validSchedule[courses: Student -> Course] {
	all stu: Student {
		#stu.courses > 2
		stu.core in stu.courses
		all disj c1, c2: stu.courses | not conflict[c1, c2]
	}
}

// Case 2.1
run MaxInterests1 {
	validSchedule[courses]
	all stu: Student | maxsome stu.interests & stu.courses
}
