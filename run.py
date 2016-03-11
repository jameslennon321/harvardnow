from flask import Flask, request, redirect
import twilio.twiml
import LaundryScrape, shuttle

app = Flask(__name__)

box = [
    {'service': 'L', 'roomid':'1362520', 'machinetype':'washer', 'label': 'DUNSTER HOUSE K Washers', 'tags': ['DUNSTER', 'HOUSE', 'K', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362520', 'machinetype':'dryer', 'label': 'DUNSTER HOUSE K Dryers', 'tags': ['DUNSTER', 'HOUSE', 'K', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362521', 'machinetype':'washer', 'label': 'DUNSTER HOUSE G Washers', 'tags': ['DUNSTER', 'HOUSE', 'G', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362521', 'machinetype':'dryer', 'label': 'DUNSTER HOUSE G Dryers', 'tags': ['DUNSTER', 'HOUSE', 'G', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'144633', 'machinetype':'washer', 'label': '10 DEWOLFE STREET Washers', 'tags': ['10', 'DEWOLFE', 'STREET', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'144633', 'machinetype':'dryer', 'label': '10 DEWOLFE STREET Dryers', 'tags': ['10', 'DEWOLFE', 'STREET', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362589', 'machinetype':'washer', 'label': 'STOUGHTON HALL Washers', 'tags': ['STOUGHTON', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362589', 'machinetype':'dryer', 'label': 'STOUGHTON HALL Dryers', 'tags': ['STOUGHTON', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362540', 'machinetype':'washer', 'label': 'CABOT HOUSE - BRIGGS HALL Washers', 'tags': ['CABOT', 'HOUSE', '-', 'BRIGGS', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362540', 'machinetype':'dryer', 'label': 'CABOT HOUSE - BRIGGS HALL Dryers', 'tags': ['CABOT', 'HOUSE', '-', 'BRIGGS', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362515', 'machinetype':'washer', 'label': '1202 MASS AVE 4TH FLR LR Washers', 'tags': ['1202', 'MASS', 'AVE', '4TH', 'FLR', 'LR', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362515', 'machinetype':'dryer', 'label': '1202 MASS AVE 4TH FLR LR Dryers', 'tags': ['1202', 'MASS', 'AVE', '4TH', 'FLR', 'LR', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362531', 'machinetype':'washer', 'label': 'NEW QUINCY 6TH FLOOR Washers', 'tags': ['NEW', 'QUINCY', '6TH', 'FLOOR', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362531', 'machinetype':'dryer', 'label': 'NEW QUINCY 6TH FLOOR Dryers', 'tags': ['NEW', 'QUINCY', '6TH', 'FLOOR', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362551', 'machinetype':'washer', 'label': 'CURRIER HOUSE - GILBERT HALL Washers', 'tags': ['CURRIER', 'HOUSE', '-', 'GILBERT', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362551', 'machinetype':'dryer', 'label': 'CURRIER HOUSE - GILBERT HALL Dryers', 'tags': ['CURRIER', 'HOUSE', '-', 'GILBERT', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362513', 'machinetype':'washer', 'label': 'PFORZHEIMER HOUSE - COMSTOCK HALL Washers', 'tags': ['PFORZHEIMER','PFOHO', 'HOUSE', '-', 'COMSTOCK', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362513', 'machinetype':'dryer', 'label': 'PFORZHEIMER HOUSE - COMSTOCK HALL Dryers', 'tags': ['PFORZHEIMER','PFOHO', 'HOUSE', '-', 'COMSTOCK', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362541', 'machinetype':'washer', 'label': 'HURLBUT HALL Washers', 'tags': ['HURLBUT', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362541', 'machinetype':'dryer', 'label': 'HURLBUT HALL Dryers', 'tags': ['HURLBUT', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362515', 'machinetype':'washer', 'label': '22 PRESCOTT ST Washers', 'tags': ['22', 'PRESCOTT', 'ST', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362515', 'machinetype':'dryer', 'label': '22 PRESCOTT ST Dryers', 'tags': ['22', 'PRESCOTT', 'ST', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362530', 'machinetype':'washer', 'label': 'LEVERETT HOUSE MCKINLOCK Washers', 'tags': ['LEVERETT', 'HOUSE', 'MCKINLOCK', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362530', 'machinetype':'dryer', 'label': 'LEVERETT HOUSE MCKINLOCK Dryers', 'tags': ['LEVERETT', 'HOUSE', 'MCKINLOCK', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362514', 'machinetype':'washer', 'label': 'PFORZHEIMER HOUSE - MOORS HALL Washers', 'tags': ['PFORZHEIMER','PFOHO', 'HOUSE', '-', 'MOORS', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362514', 'machinetype':'dryer', 'label': 'PFORZHEIMER HOUSE - MOORS HALL Dryers', 'tags': ['PFORZHEIMER','PFOHO', 'HOUSE', '-', 'MOORS', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362549', 'machinetype':'washer', 'label': 'PFORZHEIMER HOUSE - HOLMES HALL Washers', 'tags': ['PFORZHEIMER','PFOHO', 'HOUSE', '-', 'HOLMES', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362549', 'machinetype':'dryer', 'label': 'PFORZHEIMER HOUSE - HOLMES HALL Dryers', 'tags': ['PFORZHEIMER','PFOHO', 'HOUSE', '-', 'HOLMES', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362557', 'machinetype':'washer', 'label': 'PFORZHEIMER HOUSE - JORDAN SOUTH Washers', 'tags': ['PFORZHEIMER','PFOHO', 'HOUSE', '-', 'JORDAN', 'SOUTH', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362557', 'machinetype':'dryer', 'label': 'PFORZHEIMER HOUSE - JORDAN SOUTH Dryers', 'tags': ['PFORZHEIMER','PFOHO', 'HOUSE', '-', 'JORDAN', 'SOUTH', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362585', 'machinetype':'washer', 'label': 'CURRIER HOUSE - DANIELS HALL Washers', 'tags': ['CURRIER', 'HOUSE', '-', 'DANIELS', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362585', 'machinetype':'dryer', 'label': 'CURRIER HOUSE - DANIELS HALL Dryers', 'tags': ['CURRIER', 'HOUSE', '-', 'DANIELS', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362546', 'machinetype':'washer', 'label': 'ADAMS HOUSE Washers', 'tags': ['ADAMS', 'HOUSE', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362546', 'machinetype':'dryer', 'label': 'ADAMS HOUSE Dryers', 'tags': ['ADAMS', 'HOUSE', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362528', 'machinetype':'washer', 'label': 'LOWELL HOUSE G  Washers', 'tags': ['LOWELL', 'HOUSE', 'G', '', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362528', 'machinetype':'dryer', 'label': 'LOWELL HOUSE G  Dryers', 'tags': ['LOWELL', 'HOUSE', 'G', '', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362515', 'machinetype':'washer', 'label': '1201 MASS AVE 3RD FLR LR Washers', 'tags': ['1201', 'MASS', 'AVE', '3RD', 'FLR', 'LR', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362515', 'machinetype':'dryer', 'label': '1201 MASS AVE 3RD FLR LR Dryers', 'tags': ['1201', 'MASS', 'AVE', '3RD', 'FLR', 'LR', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362514', 'machinetype':'washer', 'label': '24 PRESCOTT ST Washers', 'tags': ['24', 'PRESCOTT', 'ST', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362514', 'machinetype':'dryer', 'label': '24 PRESCOTT ST Dryers', 'tags': ['24', 'PRESCOTT', 'ST', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'014711', 'machinetype':'washer', 'label': '8 PLYMPTON STREET Washers', 'tags': ['8', 'PLYMPTON', 'STREET', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'014711', 'machinetype':'dryer', 'label': '8 PLYMPTON STREET Dryers', 'tags': ['8', 'PLYMPTON', 'STREET', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362527', 'machinetype':'washer', 'label': 'LEVERETT HOUSE G TOWER Washers', 'tags': ['LEVERETT', 'HOUSE', 'G', 'TOWER', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362527', 'machinetype':'dryer', 'label': 'LEVERETT HOUSE G TOWER Dryers', 'tags': ['LEVERETT', 'HOUSE', 'G', 'TOWER', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362588', 'machinetype':'washer', 'label': 'THAYER HALL Washers', 'tags': ['THAYER', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362588', 'machinetype':'dryer', 'label': 'THAYER HALL Dryers', 'tags': ['THAYER', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362537', 'machinetype':'washer', 'label': 'CABOT HOUSE - ELLIOT HALL Washers', 'tags': ['CABOT', 'HOUSE', '-', 'ELLIOT', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362537', 'machinetype':'dryer', 'label': 'CABOT HOUSE - ELLIOT HALL Dryers', 'tags': ['CABOT', 'HOUSE', '-', 'ELLIOT', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362547', 'machinetype':'washer', 'label': 'APLEY COURT Washers', 'tags': ['APLEY', 'COURT', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362547', 'machinetype':'dryer', 'label': 'APLEY COURT Dryers', 'tags': ['APLEY', 'COURT', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362525', 'machinetype':'washer', 'label': 'KIRKLAND HOUSE J Washers', 'tags': ['KIRKLAND', 'HOUSE', 'J', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362525', 'machinetype':'dryer', 'label': 'KIRKLAND HOUSE J Dryers', 'tags': ['KIRKLAND', 'HOUSE', 'J', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362554', 'machinetype':'washer', 'label': 'PFORZHEIMER HOUSE - WOLBACH HALL Washers', 'tags': ['PFORZHEIMER','PFOHO', 'HOUSE', '-', 'WOLBACH', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362554', 'machinetype':'dryer', 'label': 'PFORZHEIMER HOUSE - WOLBACH HALL Dryers', 'tags': ['PFORZHEIMER','PFOHO', 'HOUSE', '-', 'WOLBACH', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362529', 'machinetype':'washer', 'label': 'LOWELL HOUSE D Washers', 'tags': ['LOWELL', 'HOUSE', 'D', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362529', 'machinetype':'dryer', 'label': 'LOWELL HOUSE D Dryers', 'tags': ['LOWELL', 'HOUSE', 'D', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362552', 'machinetype':'washer', 'label': 'CURRIER HOUSE - TUCHMAN HALL Washers', 'tags': ['CURRIER', 'HOUSE', '-', 'TUCHMAN', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362552', 'machinetype':'dryer', 'label': 'CURRIER HOUSE - TUCHMAN HALL Dryers', 'tags': ['CURRIER', 'HOUSE', '-', 'TUCHMAN', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362533', 'machinetype':'washer', 'label': '1306 MASS AVE Washers', 'tags': ['1306', 'MASS', 'AVE', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362533', 'machinetype':'dryer', 'label': '1306 MASS AVE Dryers', 'tags': ['1306', 'MASS', 'AVE', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362593', 'machinetype':'washer', 'label': 'STONE HALL  Washers', 'tags': ['QUINCY','STONE', 'HALL', '', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362593', 'machinetype':'dryer', 'label': 'STONE HALL  Dryers', 'tags': ['QUINCY','STONE', 'HALL', '', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'136259', 'machinetype':'washer', 'label': 'WELD HALL Washers', 'tags': ['WELD', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'136259', 'machinetype':'dryer', 'label': 'WELD HALL Dryers', 'tags': ['WELD', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'144634', 'machinetype':'washer', 'label': '20 DEWOLFE STREET Washers', 'tags': ['20', 'DEWOLFE', 'STREET', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'144634', 'machinetype':'dryer', 'label': '20 DEWOLFE STREET Dryers', 'tags': ['20', 'DEWOLFE', 'STREET', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362526', 'machinetype':'washer', 'label': 'LEVERETT HOUSE F TOWER Washers', 'tags': ['LEVERETT', 'HOUSE', 'F', 'TOWER', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362526', 'machinetype':'dryer', 'label': 'LEVERETT HOUSE F TOWER Dryers', 'tags': ['LEVERETT', 'HOUSE', 'F', 'TOWER', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362523', 'machinetype':'washer', 'label': 'ELIOT HOUSE J Washers', 'tags': ['ELIOT', 'HOUSE', 'J', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362523', 'machinetype':'dryer', 'label': 'ELIOT HOUSE J Dryers', 'tags': ['ELIOT', 'HOUSE', 'J', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362584', 'machinetype':'washer', 'label': 'CANADAY HALL Washers', 'tags': ['CANADAY', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362584', 'machinetype':'dryer', 'label': 'CANADAY HALL Dryers', 'tags': ['CANADAY', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362539', 'machinetype':'washer', 'label': 'PFORZHEIMER HOUSE - JORDAN NORTH Washers', 'tags': ['PFORZHEIMER','PFOHO', 'HOUSE', '-', 'JORDAN', 'NORTH', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362539', 'machinetype':'dryer', 'label': 'PFORZHEIMER HOUSE - JORDAN NORTH Dryers', 'tags': ['PFORZHEIMER','PFOHO', 'HOUSE', '-', 'JORDAN', 'NORTH', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362510', 'machinetype':'washer', 'label': 'CURRIER HOUSE - BINGHAM HALL Washers', 'tags': ['CURRIER', 'HOUSE', '-', 'BINGHAM', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362510', 'machinetype':'dryer', 'label': 'CURRIER HOUSE - BINGHAM HALL Dryers', 'tags': ['CURRIER', 'HOUSE', '-', 'BINGHAM', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362518', 'machinetype':'washer', 'label': 'WIGG Washers', 'tags': ['WIGG', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362518', 'machinetype':'dryer', 'label': 'WIGG Dryers', 'tags': ['WIGG', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362535', 'machinetype':'washer', 'label': 'WINTHROP - STANDISH Washers', 'tags': ['WINTHROP', '-', 'STANDISH', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362535', 'machinetype':'dryer', 'label': 'WINTHROP - STANDISH Dryers', 'tags': ['WINTHROP', '-', 'STANDISH', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362511', 'machinetype':'washer', 'label': 'CABOT HOUSE - BERTRAM HALL Washers', 'tags': ['CABOT', 'HOUSE', '-', 'BERTRAM', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362511', 'machinetype':'dryer', 'label': 'CABOT HOUSE - BERTRAM HALL Dryers', 'tags': ['CABOT', 'HOUSE', '-', 'BERTRAM', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362545', 'machinetype':'washer', 'label': 'KIRKLAND HOUSE G Washers', 'tags': ['KIRKLAND', 'HOUSE', 'G', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362545', 'machinetype':'dryer', 'label': 'KIRKLAND HOUSE G Dryers', 'tags': ['KIRKLAND', 'HOUSE', 'G', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362515', 'machinetype':'washer', 'label': '20 PRESCOTT ST Washers', 'tags': ['20', 'PRESCOTT', 'ST', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362515', 'machinetype':'dryer', 'label': '20 PRESCOTT ST Dryers', 'tags': ['20', 'PRESCOTT', 'ST', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362518', 'machinetype':'washer', 'label': 'WIGGLESWORTH HALL Washers', 'tags': ['WIGGLESWORTH', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362518', 'machinetype':'dryer', 'label': 'WIGGLESWORTH HALL Dryers', 'tags': ['WIGGLESWORTH', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362586', 'machinetype':'washer', 'label': 'LOWELL HOUSE N Washers', 'tags': ['LOWELL', 'HOUSE', 'N', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362586', 'machinetype':'dryer', 'label': 'LOWELL HOUSE N Dryers', 'tags': ['LOWELL', 'HOUSE', 'N', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362516', 'machinetype':'washer', 'label': 'GREENOUGH HALL Washers', 'tags': ['GREENOUGH', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362516', 'machinetype':'dryer', 'label': 'GREENOUGH HALL Dryers', 'tags': ['GREENOUGH', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362555', 'machinetype':'washer', 'label': 'CLAVERLY HALL Washers', 'tags': ['CLAVERLY', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362555', 'machinetype':'dryer', 'label': 'CLAVERLY HALL Dryers', 'tags': ['CLAVERLY', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362532', 'machinetype':'washer', 'label': 'NEW QUINCY BASEMENT STUDENT LAUNDRY Washers', 'tags': ['NEW', 'QUINCY', 'BASEMENT', 'STUDENT', 'LAUNDRY', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362532', 'machinetype':'dryer', 'label': 'NEW QUINCY BASEMENT STUDENT LAUNDRY Dryers', 'tags': ['NEW', 'QUINCY', 'BASEMENT', 'STUDENT', 'LAUNDRY', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362534', 'machinetype':'washer', 'label': '65 MOUNT AUBURN STREET Washers', 'tags': ['65', 'MOUNT', 'AUBURN', 'STREET', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362534', 'machinetype':'dryer', 'label': '65 MOUNT AUBURN STREET Dryers', 'tags': ['65', 'MOUNT', 'AUBURN', 'STREET', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362536', 'machinetype':'washer', 'label': 'WINTHROP - GORE Washers', 'tags': ['WINTHROP', '-', 'GORE', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362536', 'machinetype':'dryer', 'label': 'WINTHROP - GORE Dryers', 'tags': ['WINTHROP', '-', 'GORE', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362548', 'machinetype':'washer', 'label': 'MATHER HOUSE HIGH RISE Washers', 'tags': ['MATHER', 'HOUSE', 'HIGH', 'RISE', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362548', 'machinetype':'dryer', 'label': 'MATHER HOUSE HIGH RISE Dryers', 'tags': ['MATHER', 'HOUSE', 'HIGH', 'RISE', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362512', 'machinetype':'washer', 'label': 'CABOT HOUSE - WHITMAN HALL Washers', 'tags': ['CABOT', 'HOUSE', '-', 'WHITMAN', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362512', 'machinetype':'dryer', 'label': 'CABOT HOUSE - WHITMAN HALL Dryers', 'tags': ['CABOT', 'HOUSE', '-', 'WHITMAN', 'HALL', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362556', 'machinetype':'washer', 'label': 'MATHER HOUSE LOW RISE Washers', 'tags': ['MATHER', 'HOUSE', 'LOW', 'RISE', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'L', 'roomid':'1362556', 'machinetype':'dryer', 'label': 'MATHER HOUSE LOW RISE Dryers', 'tags': ['MATHER', 'HOUSE', 'LOW', 'RISE', 'LAUNDRY', 'WASHERS', 'WASHER']},
    {'service': 'S-S', 'stopid': '4070614' , 'label': 'Quad Shuttle Stop', 'tags':['QUAD', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4070630' , 'label': 'Mass Ave & Garden St Shuttle Stop', 'tags':['MASS', 'AVE', '&', 'GARDEN', 'ST', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4070634' , 'label': 'Memorial Hall Shuttle Stop', 'tags':['MEMORIAL', 'HALL', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4070638' , 'label': 'Lamont Library Shuttle Stop', 'tags':['LAMONT', 'LIBRARY', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4070642' , 'label': 'Widener Gate Shuttle Stop', 'tags':['WIDENER', 'GATE', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4070670' , 'label': 'Inn at Harvard Shuttle Stop', 'tags':['INN', 'AT', 'HARVARD', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4109006' , 'label': 'Law School Shuttle Stop', 'tags':['LAW', 'SCHOOL', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4125502' , 'label': 'Winthrop House Shuttle Stop', 'tags':['WINTHROP', 'HOUSE', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4130382' , 'label': 'Mather House Shuttle Stop', 'tags':['MATHER', 'HOUSE', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4166978' , 'label': 'Peabody Terrace Shuttle Stop', 'tags':['PEABODY', 'TERRACE', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190630' , 'label': 'Kennedy (Temporary Stop) Shuttle Stop', 'tags':['KENNEDY', '(TEMPORARY', 'STOP)', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190632' , 'label': 'Maxwell Dworkin Shuttle Stop', 'tags':['MAXWELL', 'DWORKIN', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190634' , 'label': 'Harvard Square Shuttle Stop', 'tags':['HARVARD', 'SQUARE', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190636' , 'label': 'Stadium Shuttle Stop', 'tags':['STADIUM', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190638' , 'label': 'HiLab-HBS Shuttle Stop', 'tags':['HILAB-HBS', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190640' , 'label': 'Soldiers Field Park Shuttle Stop', 'tags':['SOLDIERS', 'FIELD', 'PARK', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190642' , 'label': 'Kennedy School Shuttle Stop', 'tags':['KENNEDY', 'SCHOOL', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190644' , 'label': 'i-Lab (Temporary) Shuttle Stop', 'tags':['I-LAB', '(TEMPORARY)', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190646' , 'label': 'Jordan Field Shuttle Stop', 'tags':['JORDAN', 'FIELD', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190648' , 'label': 'Stadium Complex (Gate #8) Shuttle Stop', 'tags':['STADIUM', 'COMPLEX', '(GATE', '#8)', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190650' , 'label': 'DeWolfe St. at Mill St. Area Shuttle Stop', 'tags':['DEWOLFE', 'ST.', 'AT', 'MILL', 'ST.', 'AREA', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190652' , 'label': 'Lamont Library Gate Shuttle Stop', 'tags':['LAMONT', 'LIBRARY', 'GATE', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190654' , 'label': 'Garden St. at Mason St. Shuttle Stop', 'tags':['GARDEN', 'ST.', 'AT', 'MASON', 'ST.', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190656' , 'label': '175 North Harvard Shuttle Stop', 'tags':['175', 'NORTH', 'HARVARD', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190660' , 'label': 'Soldiers Field Park (Temporary) Shuttle Stop', 'tags':['SOLDIERS', 'FIELD', 'PARK', '(TEMPORARY)', 'SHUTTLE', 'STOP']},
    {'service': 'S-S', 'stopid': '4190662' , 'label': 'Barry\'s Corner Shuttle Stop', 'tags':["BARRY\'S", 'CORNER', "BARRY", 'SHUTTLE', 'STOP']},
    {'service': 'S-R', 'routeid': '4003894' , 'label': 'Quad Express Shuttle Route', 'tags':['QUAD', 'EXPRESS', 'SHUTTLE', 'ROUTE']},
    {'service': 'S-R', 'routeid': '4003906' , 'label': 'River House A Shuttle Route', 'tags':['RIVER', 'HOUSE', 'A', 'SHUTTLE', 'ROUTE']},
    {'service': 'S-R', 'routeid': '4003910' , 'label': 'River House B Shuttle Route', 'tags':['RIVER', 'HOUSE', 'B', 'SHUTTLE', 'ROUTE']},
    {'service': 'S-R', 'routeid': '4003914' , 'label': 'Quad Yard Express Shuttle Route', 'tags':['QUAD', 'YARD', 'EXPRESS', 'SHUTTLE', 'ROUTE']},
    {'service': 'S-R', 'routeid': '4003934' , 'label': 'River House C Shuttle Route', 'tags':['RIVER', 'HOUSE', 'C', 'SHUTTLE', 'ROUTE']},
    {'service': 'S-R', 'routeid': '4003938' , 'label': 'Extended Overnight Shuttle Route', 'tags':['EXTENDED', 'OVERNIGHT', 'SHUTTLE', 'ROUTE']},
    {'service': 'S-R', 'routeid': '4007272' , 'label': 'Barry\'s Corner Shuttle Route', 'tags':["BARRY'S",'BARRY', 'CORNER', 'SHUTTLE', 'ROUTE']},
    {'service': 'S-R', 'routeid': '4007610' , 'label': 'Quad Stadium Express Shuttle Route', 'tags':['QUAD', 'STADIUM', 'EXPRESS', 'SHUTTLE', 'ROUTE']},
    {'service': 'S-R', 'routeid': '4007650' , 'label': 'Allston Campus Express Shuttle Route', 'tags':['ALLSTON', 'CAMPUS', 'EXPRESS', 'SHUTTLE', 'ROUTE']}
]

def filter(tag,cmds=box):
    return [cmd for cmd in cmds if tag in cmd['tags']]

def eval(cmd):
    if cmd['service'] == 'L':
        return cmd['label']+'\n'+LaundryScrape.machines_to_string(LaundryScrape.getMachines(cmd['roomid'],cmd['machinetype']))
    elif cmd['service'] == 'S-S':
        return cmd['label']+'\n'+shuttle.arrivalsStopToString(shuttle.arrivalsAtStopID(cmd['stopid']))
    elif cmd['service'] == 'S-R':
        return cmd['label']+'\n'+shuttle.arrivalsRouteToString(shuttle.arrivalsAtRouteId(cmd['routeid']))
    
@app.route("/", methods=['GET', 'POST'])
def response():
    resp = twilio.twiml.Response()
    incoming = request.values.get('Body',None)
    body = ""

    words = set(incoming.upper().split(" "))
    print words
    started = False
    results = box
    for word in words:
        r = filter(word,results)
        if r == []:
            break
        else:
            started = True
            results = r
    if len(results)>6:
        body = "Sorry, that's too many requests."
    elif not started:
        body = "Sorry, I don't know what that is."
    else:
        body = "\n".join(['\n'+eval(cmd) for cmd in results])

    
    # mtype = "washer"
    # if ("dryer" in words or "dryers" in words) and ("washer" not in words and "washers" not in words):
    #     mtype = "dryer"

    # lost = False
    # found = False
    # for word in words:
    #     print word
    #     machines = LaundryScrape.getMachines(word,mtype)
    #     print machines
    #     if type(machines) is str:
    #         message = machines.split('|')
    #         messagetype = message.pop(0)
    #         if messagetype == "MULTIPLE" and not found:
    #             lost = True
    #             body+= "There are multiple laundry rooms in "+message.pop(0)
    #             body+= "\nTry one of these: \n"
    #             for room in message:
    #                 body+= room+"\n"
    #     else:
    #         if not found:
    #             body = ""
    #             found = True
    #         body+= word.upper()+" "+mtype.upper()+"S:\n"
    #         body+=LaundryScrape.machines_to_string(machines)
            
    # if not (lost or found):
    #     if "laundry" in incoming.lower():
    #         body = LaundryScrape.room_names()
    #     else :
    #         body = "Sorry, I don't know what that is."

    resp.message(body)
    return str(resp)



if __name__ == "__main__":
    app.run(debug=True)
