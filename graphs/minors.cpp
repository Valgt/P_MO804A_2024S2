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
    vector<pair<int, int>> edges;
    for (int tc=0; tc<T; ++tc) {
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
        edges.push_back({u, v});
    }
    vector<bool> e(T, 1);
    for (int i=0; i<50; ++i) {
        e[i] = 0;
    }
    mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
    shuffle(e.begin(), e.end(), rng);
    for (int i=0; i<m; ++i) {
        rnk[i] = 0;
        lnk[i] = i;
    }
    int co = m;
    shuffle(edges.begin(), edges.end(), rng);
    for (int i=0; i<T; ++i) {
        if (e[i] == 0) continue;
        auto [u, v] = edges[i];
        if (get(u) != get(v)) {
            merge(u, v);
            co--;
        }
        if (co <= 100) break;
    }
    set<pair<int, int>> se; 
    for (int i=0; i<T; ++i) {
        auto [u, v] = edges[i];
        u = get(u);
        v = get(v);
        if (u == v) continue;
        if (se.count({u, v})) continue;
        se.insert({u, v});
        se.insert({v, u});
        cout << u << ' ' << v << '\n';
    }

    return 0;
}