import api_client
import json

def verify():
    print("Fetching matches...")
    matches = api_client.fetch_matches()
    
    if not matches:
        print("No matches returned or API error.")
        return

    print(f"Total Matches: {len(matches)}")
    
    live = api_client.get_live_matches()
    upcoming = api_client.get_upcoming_matches()
    ended = api_client.get_ended_matches()
    
    print(f"\n🔴 Live Matches: {len(live) if live else 0}")
    if live:
        for m in live:
            print(f" - {m.get('match', 'N/A')} (Score len: {len(m.get('scores', []))})")

    print(f"\n⏳ Upcoming Matches: {len(upcoming) if upcoming else 0}")
    if upcoming:
        for m in upcoming:
            print(f" - {m.get('match', 'N/A')} (Score len: {len(m.get('scores', []))})")
            
    print(f"\n🏁 Ended Matches: {len(ended) if ended else 0}")
    if ended:
        for m in ended:
            print(f" - {m.get('match', 'N/A')} (Score len: {len(m.get('scores', []))})")

if __name__ == "__main__":
    verify()
