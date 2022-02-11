auto = [{
            "Step_Type": "Straight", #Step_Type says whether we will be driving forward, or turning in this step
            "Distance": 3, # How far we need to move forward in this step
            "Angle": 0, # What angle we need to turn to in this step
            "Threshold_Value": .1, # To complete the step, we need to be within the threshold feet of the target distance
            "Threshold_Time": 1, # Once we are in the threshold for this amount of time, we move to the next step
        },{ #top left turn
            "Step_Type": "Turn",
            "Distance": 0,
            "Angle": 90,
            "Threshold_Value": 5,
            "Threshold_Time": 1,
        },{
            "Step_Type": "Straight",
            "Distance": 3,
            "Angle": 90,
            "Threshold_Value": .1,
            "Threshold_Time": 1,
        },{# top right turn
            "Step_Type": "Turn",
            "Distance": 0,
            "Angle": 180,
            "Threshold_Value": 5,
            "Threshold_Time": 1,
        },{
            "Step_Type": "Straight",
            "Distance": 3,
            "Angle": 180,
            "Threshold_Value": .1,
            "Threshold_Time": 1,
        },{#bottom right turn
            "Step_Type": "Turn",
            "Distance": 0,
            "Angle": -90,
            "Threshold_Value": 5,
            "Threshold_Time": 1,
        },{
            "Step_Type": "Straight",
            "Distance": 3,
            "Angle": -90,
            "Threshold_Value": .1,
            "Threshold_Time": 1,
        },{#bottome left turn back to orientation at the start
            "Step_Type": "Turn",
            "Distance": 0,
            "Angle": 0,
            "Threshold_Value": 5,
            "Threshold_Time": 1,
        },
        ]