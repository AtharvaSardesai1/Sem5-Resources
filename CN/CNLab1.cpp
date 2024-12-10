#include <iostream>
#include <string>
#include <bitset>
#include <sstream>
#include <vector>
#include <arpa/inet.h>

using namespace std;

string findSubnetMask(int subnetMask) {
    uint32_t mask = 0xFFFFFFFF << (32 - subnetMask); // left shift by (32 - subnetMask)
    struct in_addr addr;
    addr.s_addr = htonl(mask); // convert to network byte order
    return inet_ntoa(addr); // convert to dotted-decimal string
}

vector<string> findNetworkId(const string& ipAdd, const string& subnetMask) {
    struct in_addr ipAddr, subnetAddr, networkAddr, broadcastAddr;
    inet_aton(ipAdd.c_str(), &ipAddr);
    inet_aton(subnetMask.c_str(), &subnetAddr);

    networkAddr.s_addr = ipAddr.s_addr & subnetAddr.s_addr;
    broadcastAddr.s_addr = ipAddr.s_addr | ~subnetAddr.s_addr;

    vector<string> result;
    result.push_back(inet_ntoa(networkAddr));
    result.push_back(inet_ntoa(broadcastAddr));

    return result;
}

vector<string> findUsableRange(const string& networkId, const string& broadcastId) {
    struct in_addr netAddr, broadAddr, firstUsable, lastUsable;
    inet_aton(networkId.c_str(), &netAddr);
    inet_aton(broadcastId.c_str(), &broadAddr);

    firstUsable.s_addr = netAddr.s_addr + htonl(1);
    lastUsable.s_addr = broadAddr.s_addr - htonl(1);

    vector<string> result;
    result.push_back(inet_ntoa(firstUsable));
    result.push_back(inet_ntoa(lastUsable));

    return result;
}

int main() {
    while (true) {
        cout << "Main Menu:" << endl;
        cout << "1. Get Subnet Mask" << endl;
        cout << "2. Get Network ID and Broadcast ID" << endl;
        cout << "3. Get Usable Range" << endl;
        cout << "4. Exit" << endl;
        cout << "Enter your choice: ";
        int choice;
        cin >> choice;

        if (choice == 4) {
            break;
        }

        cout << "Enter the IP address with subnet (e.g., 192.168.1.1/24): ";
        string input;
        cin >> input;

        size_t slashPos = input.find('/');
        string ipAdd = input.substr(0, slashPos);
        int subnetNum = stoi(input.substr(slashPos + 1));

        string subnetMask = findSubnetMask(subnetNum);
        vector<string> netBroadArray = findNetworkId(ipAdd, subnetMask);
        string networkId = netBroadArray[0];
        string broadcastId = netBroadArray[1];

        switch (choice) {
            case 1:
                cout << "The subnet mask for " << input << " is " << subnetMask << endl;
                break;
            case 2:
                cout << "Network ID: " << networkId << endl;
                cout << "Broadcast ID: " << broadcastId << endl;
                break;
            case 3:
                {
                    vector<string> usableRange = findUsableRange(networkId, broadcastId);
                    cout << "Usable IP Range: " << usableRange[0] << " to " << usableRange[1] << endl;
                }
                break;
            default:
                cout << "Invalid choice. Please try again." << endl;
        }
    }

    return 0;
}
