#!/bin/bash

IP=10.0.3.145

echo '--- Polling 0x0200 (512) to 0x0275 (629) count 118 ---'
mbpoll -0 -r 512 -c 118 -1 $IP || echo 'Failed to poll 0x0200'

echo '--- Polling 0x0500 (1280) to 0x0576 (1398) count 119 ---'
mbpoll -0 -r 1280 -c 119 -1 $IP || echo 'Failed to poll 0x0500'

echo '--- Polling 0x0600 (1536) to 0x0677 (1655) count 120 ---'
mbpoll -0 -r 1536 -c 120 -1 $IP || echo 'Failed to poll 0x0600'

echo '--- Polling 0x0F01 (3841) to 0x0F31 (3889) count 49 ---'
mbpoll -0 -r 3841 -c 49 -1 $IP || echo 'Failed to poll 0x0F01'

echo '--- Polling 0x1101 (4353) to 0x117D (4477) count 125 ---'
mbpoll -0 -r 4353 -c 125 -1 $IP || echo 'Failed to poll 0x1101'

echo '--- Polling 0x117E (4478) to 0x1180 (4480) count 3 ---'
mbpoll -0 -r 4478 -c 3 -1 $IP || echo 'Failed to poll 0x117E'

echo '--- Polling 0x1501 (5377) to 0x157D (5501) count 125 ---'
mbpoll -0 -r 5377 -c 125 -1 $IP || echo 'Failed to poll 0x1501'

echo '--- Polling 0x157E (5502) to 0x15FA (5626) count 125 ---'
mbpoll -0 -r 5502 -c 125 -1 $IP || echo 'Failed to poll 0x157E'

echo '--- Polling 0x15FB (5627) to 0x1618 (5656) count 30 ---'
mbpoll -0 -r 5627 -c 30 -1 $IP || echo 'Failed to poll 0x15FB'

echo '--- Polling 0x2400 (9216) to 0x247C (9340) count 125 ---'
mbpoll -0 -r 9216 -c 125 -1 $IP || echo 'Failed to poll 0x2400'

echo '--- Polling 0x247D (9341) to 0x24F9 (9465) count 125 ---'
mbpoll -0 -r 9341 -c 125 -1 $IP || echo 'Failed to poll 0x247D'

echo '--- Polling 0x24FA (9466) to 0x2576 (9590) count 125 ---'
mbpoll -0 -r 9466 -c 125 -1 $IP || echo 'Failed to poll 0x24FA'

echo '--- Polling 0x2577 (9591) to 0x25F3 (9715) count 125 ---'
mbpoll -0 -r 9591 -c 125 -1 $IP || echo 'Failed to poll 0x2577'

echo '--- Polling 0x25F4 (9716) to 0x2670 (9840) count 125 ---'
mbpoll -0 -r 9716 -c 125 -1 $IP || echo 'Failed to poll 0x25F4'

echo '--- Polling 0x2671 (9841) to 0x26ED (9965) count 125 ---'
mbpoll -0 -r 9841 -c 125 -1 $IP || echo 'Failed to poll 0x2671'

echo '--- Polling 0x26EE (9966) to 0x276A (10090) count 125 ---'
mbpoll -0 -r 9966 -c 125 -1 $IP || echo 'Failed to poll 0x26EE'

echo '--- Polling 0x276B (10091) to 0x27E7 (10215) count 125 ---'
mbpoll -0 -r 10091 -c 125 -1 $IP || echo 'Failed to poll 0x276B'

echo '--- Polling 0x27E8 (10216) to 0x27E8 (10216) count 1 ---'
mbpoll -0 -r 10216 -c 1 -1 $IP || echo 'Failed to poll 0x27E8'

echo '--- Polling 0x3500 (13568) to 0x357C (13692) count 125 ---'
mbpoll -0 -r 13568 -c 125 -1 $IP || echo 'Failed to poll 0x3500'

echo '--- Polling 0x357D (13693) to 0x35F9 (13817) count 125 ---'
mbpoll -0 -r 13693 -c 125 -1 $IP || echo 'Failed to poll 0x357D'

echo '--- Polling 0x35FA (13818) to 0x3676 (13942) count 125 ---'
mbpoll -0 -r 13818 -c 125 -1 $IP || echo 'Failed to poll 0x35FA'

echo '--- Polling 0x3677 (13943) to 0x36EF (14063) count 121 ---'
mbpoll -0 -r 13943 -c 121 -1 $IP || echo 'Failed to poll 0x3677'

echo '--- Polling 0x3A04 (14852) to 0x3A04 (14852) count 1 ---'
mbpoll -0 -r 14852 -c 1 -1 $IP || echo 'Failed to poll 0x3A04'

echo '--- Polling 0x4001 (16385) to 0x407D (16509) count 125 ---'
mbpoll -0 -r 16385 -c 125 -1 $IP || echo 'Failed to poll 0x4001'

echo '--- Polling 0x407E (16510) to 0x40FA (16634) count 125 ---'
mbpoll -0 -r 16510 -c 125 -1 $IP || echo 'Failed to poll 0x407E'

echo '--- Polling 0x40FB (16635) to 0x4177 (16759) count 125 ---'
mbpoll -0 -r 16635 -c 125 -1 $IP || echo 'Failed to poll 0x40FB'

echo '--- Polling 0x4178 (16760) to 0x41A7 (16807) count 48 ---'
mbpoll -0 -r 16760 -c 48 -1 $IP || echo 'Failed to poll 0x4178'

echo '--- Polling 0x4201 (16897) to 0x427D (17021) count 125 ---'
mbpoll -0 -r 16897 -c 125 -1 $IP || echo 'Failed to poll 0x4201'

echo '--- Polling 0x4401 (17409) to 0x447D (17533) count 125 ---'
mbpoll -0 -r 17409 -c 125 -1 $IP || echo 'Failed to poll 0x4401'

echo '--- Polling 0x447E (17534) to 0x44E9 (17641) count 108 ---'
mbpoll -0 -r 17534 -c 108 -1 $IP || echo 'Failed to poll 0x447E'

echo '--- Polling 0x4501 (17665) to 0x4571 (17777) count 113 ---'
mbpoll -0 -r 17665 -c 113 -1 $IP || echo 'Failed to poll 0x4501'

echo '--- Polling 0x4601 (17921) to 0x465A (18010) count 90 ---'
mbpoll -0 -r 17921 -c 90 -1 $IP || echo 'Failed to poll 0x4601'

echo '--- Polling 0x4801 (18433) to 0x487D (18557) count 125 ---'
mbpoll -0 -r 18433 -c 125 -1 $IP || echo 'Failed to poll 0x4801'

echo '--- Polling 0x487E (18558) to 0x48F0 (18672) count 115 ---'
mbpoll -0 -r 18558 -c 115 -1 $IP || echo 'Failed to poll 0x487E'

echo '--- Polling 0x4901 (18689) to 0x497D (18813) count 125 ---'
mbpoll -0 -r 18689 -c 125 -1 $IP || echo 'Failed to poll 0x4901'

echo '--- Polling 0x497E (18814) to 0x49FA (18938) count 125 ---'
mbpoll -0 -r 18814 -c 125 -1 $IP || echo 'Failed to poll 0x497E'

echo '--- Polling 0x49FB (18939) to 0x4A00 (18944) count 6 ---'
mbpoll -0 -r 18939 -c 6 -1 $IP || echo 'Failed to poll 0x49FB'

echo '--- Polling 0x4B01 (19201) to 0x4B48 (19272) count 72 ---'
mbpoll -0 -r 19201 -c 72 -1 $IP || echo 'Failed to poll 0x4B01'

echo '--- Polling 0x4C81 (19585) to 0x4CA0 (19616) count 32 ---'
mbpoll -0 -r 19585 -c 32 -1 $IP || echo 'Failed to poll 0x4C81'

echo '--- Polling 0x4E01 (19969) to 0x4E7D (20093) count 125 ---'
mbpoll -0 -r 19969 -c 125 -1 $IP || echo 'Failed to poll 0x4E01'

echo '--- Polling 0x4E7E (20094) to 0x4EFA (20218) count 125 ---'
mbpoll -0 -r 20094 -c 125 -1 $IP || echo 'Failed to poll 0x4E7E'

echo '--- Polling 0x4EFB (20219) to 0x4F00 (20224) count 6 ---'
mbpoll -0 -r 20219 -c 6 -1 $IP || echo 'Failed to poll 0x4EFB'

echo '--- Polling 0x5101 (20737) to 0x517D (20861) count 125 ---'
mbpoll -0 -r 20737 -c 125 -1 $IP || echo 'Failed to poll 0x5101'

echo '--- Polling 0x517E (20862) to 0x51F4 (20980) count 119 ---'
mbpoll -0 -r 20862 -c 119 -1 $IP || echo 'Failed to poll 0x517E'

echo '--- Polling 0x8000 (32768) to 0x802C (32812) count 45 ---'
mbpoll -0 -r 32768 -c 45 -1 $IP || echo 'Failed to poll 0x8000'

echo '--- Polling 0x8201 (33281) to 0x8214 (33300) count 20 ---'
mbpoll -0 -r 33281 -c 20 -1 $IP || echo 'Failed to poll 0x8201'

echo '--- Polling 0x8301 (33537) to 0x837D (33661) count 125 ---'
mbpoll -0 -r 33537 -c 125 -1 $IP || echo 'Failed to poll 0x8301'

echo '--- Polling 0x837E (33662) to 0x83C2 (33730) count 69 ---'
mbpoll -0 -r 33662 -c 69 -1 $IP || echo 'Failed to poll 0x837E'

echo '--- Polling 0x8401 (33793) to 0x8413 (33811) count 19 ---'
mbpoll -0 -r 33793 -c 19 -1 $IP || echo 'Failed to poll 0x8401'

echo '--- Polling 0x8479 (33913) to 0x84F5 (34037) count 125 ---'
mbpoll -0 -r 33913 -c 125 -1 $IP || echo 'Failed to poll 0x8479'

echo '--- Polling 0x84F6 (34038) to 0x8572 (34162) count 125 ---'
mbpoll -0 -r 34038 -c 125 -1 $IP || echo 'Failed to poll 0x84F6'

echo '--- Polling 0x8573 (34163) to 0x85C1 (34241) count 79 ---'
mbpoll -0 -r 34163 -c 79 -1 $IP || echo 'Failed to poll 0x8573'

echo '--- Polling 0x8601 (34305) to 0x867D (34429) count 125 ---'
mbpoll -0 -r 34305 -c 125 -1 $IP || echo 'Failed to poll 0x8601'

echo '--- Polling 0x867E (34430) to 0x86C1 (34497) count 68 ---'
mbpoll -0 -r 34430 -c 68 -1 $IP || echo 'Failed to poll 0x867E'

echo '--- Polling 0x8701 (34561) to 0x877D (34685) count 125 ---'
mbpoll -0 -r 34561 -c 125 -1 $IP || echo 'Failed to poll 0x8701'

echo '--- Polling 0x877E (34686) to 0x87EF (34799) count 114 ---'
mbpoll -0 -r 34686 -c 114 -1 $IP || echo 'Failed to poll 0x877E'

echo '--- Polling 0x8800 (34816) to 0x8877 (34935) count 120 ---'
mbpoll -0 -r 34816 -c 120 -1 $IP || echo 'Failed to poll 0x8800'

echo '--- Polling 0x8900 (35072) to 0x8977 (35191) count 120 ---'
mbpoll -0 -r 35072 -c 120 -1 $IP || echo 'Failed to poll 0x8900'

echo '--- Polling 0x8980 (35200) to 0x89F7 (35319) count 120 ---'
mbpoll -0 -r 35200 -c 120 -1 $IP || echo 'Failed to poll 0x8980'

echo '--- Polling 0x8A00 (35328) to 0x8A77 (35447) count 120 ---'
mbpoll -0 -r 35328 -c 120 -1 $IP || echo 'Failed to poll 0x8A00'

echo '--- Polling 0x8A80 (35456) to 0x8AF7 (35575) count 120 ---'
mbpoll -0 -r 35456 -c 120 -1 $IP || echo 'Failed to poll 0x8A80'

echo '--- Polling 0x8F00 (36608) to 0x8F1D (36637) count 30 ---'
mbpoll -0 -r 36608 -c 30 -1 $IP || echo 'Failed to poll 0x8F00'

echo '--- Polling 0xA001 (40961) to 0xA078 (41080) count 120 ---'
mbpoll -0 -r 40961 -c 120 -1 $IP || echo 'Failed to poll 0xA001'

