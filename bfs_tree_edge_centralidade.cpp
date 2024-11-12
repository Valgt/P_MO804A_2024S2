#include <bits/stdc++.h>
using namespace std;

const int maxn = 10010;
vector<int> g[maxn];
int n = 9860;
int rnk[maxn], lnk[maxn];

int get(int x) {
    return x == lnk[x] ? x : lnk[x] = get(lnk[x]);
}

void merge(int x, int y) {
    x=get(x); y=get(y);
    if (x == y) return;
    if (rnk[x] < rnk[y]) swap(x, y);
    rnk[x] += rnk[x]==rnk[y];
    lnk[y]=x;
}

std::vector<std::string> splitByComma(const std::string& input) {
    std::vector<std::string> tokens;
    std::stringstream ss(input);
    std::string token;

    while (std::getline(ss, token, ',')) { // Usa ',' como delimitador
        tokens.push_back(token);
    }

    return tokens;
}

int main() {
    string s;
    cin>>s;
    map<string, int> id;
    int m = 0;
    int T = 1291321;
    while (T--) {
        cin>>s;
        auto vs = splitByComma(s);
        assert(vs.size() == 3);

        for (int i=0; i<2; ++i) {
            if (!id.count(vs[i])) {
                id[vs[i]] = m++;
            }
        }

        int u = id[vs[0]];
        int v = id[vs[1]];
        g[u].emplace_back(v);
        g[v].emplace_back(u);
    }
    cout << "first" << endl;
    vector<pair<float, int>> as;
    for (int i=0; i<n; ++i) {
        float x;
        cin>>x;
        as.emplace_back(x, i);
    }
    cout << "correct" << endl;
    sort(as.begin(), as.end());
    vector<bool> vis(n);
    int components = n;
    vector<int> res;
    for (int i=0; i<n; ++i) lnk[i] = i;
    for (int i=0; i<n; ++i) {
        res.push_back(components);
        int u = as[i].second;
        vis[u] = 1;
        for (int v : g[u]) {
            if (!vis[v]) continue;
            if (get(u) != get(v)) {
                merge(u, v);
                components--;
            }
        }
    }
    reverse(res.begin(), res.end());
    for (int r : res) {
        cout << r << endl;
    }
    return 0;
}