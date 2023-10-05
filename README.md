# Stock Alert
It's an automate software to get realtime notification in WhatsApp, when a stock meets the criteria to BUY or SELL.<br>
This software purely focused on dividend based stocks only, which helps us to achieve financial freedom.<br>
BUY or SELL criteria only sent to WhatsApp groups, you can change code if you need in personal number.<br><br>
<u>Note:- </u>The codes supported for <b>Groww</b> urls only <br>

Buy Criteria :-<br>
- Stock ROE must be greater than 10<br>
- Stock Dividend Yield must be greater than 2%
- Day Changes must fall below -2%

Sell Criteria :-<br>
- The stocks which are already bought, must have at least 10% gain<br>
- ROE or Dividend Yield failed as per buy criteria<br>


How to get WhatsApp group id:- <br>
- Must be group admin<br>
- In WhatsApp Group details, click on <b>Invite to Group via Link</b><br>
- Now there must be a code after <u>https://chat.whatsapp.com/ </u> , copy that id to trigger notifications in WhatsApp Groups
- You can notify to multiple groups.

It also helps to get Airtel Wifi Battery Percentage, by Providing Airtel Wifi admin url. <br>


## Steps to get Realtime Stock Notification
- Install all the dependencies from req.txt
- Update the Group List and Mobile no List in <b>user_stocks_input_file.py</b>
- Put all your watchlist stocks, or invested stocks details, as mention in code comments.<br>
- Now run <b>groww_stock_alert.py</b>, to get realtime notifications.
- The software automatic stops at the end of the trade time at 15:20, with EOD(End Of Day) message to group.
- In case low internet, or any connection issue to get stock details, software automatically got stopped, with notification to the List of WhatsApp numbers.
- In that case you need to again trigger <b>groww_stock_alert.py</b>.<br>

## Steps to manually trigger EOD message
 In case of any failure to get stock details, and it's nearly to be end of the day, you can only trigger the EOD message.<br>
This notification contains two types of notification message.<br>
One is Thank you message and another one is Weekly Update.<br>
Where Thank you message can be customised in <b>user_stocks_input.py</b><br>
#### What is weekly update ?
 The stocks which meets our Buy Criteria, and lies in <b>NIFTY Next 50, Nifty Midcap 100, Nifty 50,Nifty 100 and BSE 100</b>.<br>
These stocks we can check by running <b>check_new_stocks.py</b>.<br>
It's recommended to check stocks weekly once.<br>

<u>Note:-</u> All Below steps should be updated in <b>weekly_update.py</b> only<br>
- The Date when we want to send notification should note in 'trigger_date' key. <br>
- The new stocks should be note in 'newly_added_stocks' key.<br>
- Similarly, if we get any sell notifications, we completely remove that stock from stock list. 
- And that stock should be note in 'removed_stocks' key.  
 

## Steps to check new stocks
- Need to run <b>check_new_stocks</b>, that's it.