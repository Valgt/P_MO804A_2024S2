#include <bits/stdc++.h>
using namespace std;

std::vector<std::string> splitByComma(const std::string& input) {
    std::vector<std::string> tokens;
    std::stringstream ss(input);
    std::string token;

    while (std::getline(ss, token, ',')) { // Usa ',' como delimitador
        tokens.push_back(token);
    }

    return tokens;
}

const int maxn = 1e4 + 5;
int dist[maxn][maxn];
int n = 9860;
bool vis[maxn];

int T=0;
void dfs(int x, int p) {
    T++;
    vis[x] = 1;
    for (int i=0; i<n; ++i) {
        if (dist[x][i] != 1) continue; 
        if (vis[i] || i == p) continue;
        dfs(i, x);
    }
}

vector<pair<int, int>> edges;
int pp[2][1300000];
int wp[2][1300000];
void bfs(int u) {
    vector<int> d(n, 1e9);
    queue<int> Q;
    Q.push(u);
    d[u] = 0;
    while (!Q.empty()) {
        int q = Q.front(); Q.pop();
        for (int v=0; v<n; ++v) {
            if (dist[q][v] != 1) continue;
            if (d[v] > d[q] + 1) {
                d[v] = d[q] + 1;
                Q.push(v);  
            }
        }
    }
    int t=-1;
    for (auto [u, v] : edges) {
        t++;
        if (d[u] > n || d[v] > n) continue;
        wp[0][t]++;
        wp[1][t]++;
        if (d[u] + 1 == d[v]) pp[0][t]++;
        if (d[v] + 1 == d[u]) pp[1][t]++;
    }
}

int main() {
    string s;
    cin>>s;
    map<string, int> id;
    int m = 0;
    memset(dist, 63, sizeof dist);
    for (int i=0; i<n; ++i) dist[i][i] = 0;
    while (cin>>s) {
        auto vs = splitByComma(s);

        for (int i=0; i<2; ++i) {
            if (!id.count(vs[i])) {
                id[vs[i]] = m++;
            }
        }

        int u = id[vs[0]];
        int v = id[vs[1]];
        edges.emplace_back(u, v);
        dist[u][v] = dist[v][u] = 1;
    }

    int comp = 0;
    int mx = -1;
    for (int i=0; i<n; ++i)
        if (!vis[i]) {
            T = 0;
            dfs(i, -1);
            mx = max(mx, T);
            comp++;
        }
    cout << "components: " << comp << endl;
    cout << "max component: " << mx << endl;

    for (int k=0; k<n; ++k)
        for (int i=0; i<n; ++i) {
            if ((k * n + i) % 1000000 == 0) cout << "1/100" << endl;
            if (dist[i][k] > n) continue; 
            for (int j=0; j<n; ++j) 
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
        }
    
    vector<int> cnt(n);
    for (int i=0; i<n; ++i)
        for (int j=i+1; j<n; ++j)
            if (dist[i][j] < n) {
                cnt[dist[i][j]]++;
            }
    cout << "distance frecuency: " << endl;
    for (int i=0; i<12; ++i) {
        cout << cnt[i] << endl;
    }
    vector<int> ns(n), ms(n);
    for (int i=0; i<n; ++i)
        for (int j=i; j<n; ++j) {
            if ((i * n + j) % 1000000 == 0) cout << "1/100" << endl;
            if (dist[i][j] > n) continue;
            for (int k=0; k<n; ++k) {
                if (dist[i][k] > n || dist[k][j] > n) continue;
                ms[k]++;
                if (dist[i][j] == dist[i][k] + dist[k][j]) {
                    ns[k]++;
                }
            }
        }
    cout << "centralidad nodo distribution: " << endl;
    vector<float> ww(n);
    for (int i=0; i<n; ++i) {
        ww[i] = (float)ns[i] / ms[i];
        cout << ww[i] << endl;
    }
    cout << "centralidad edge distribution: " << endl;
    for (int i=0; i<n; ++i) bfs(i);
    int t=0;
    for (auto [u, v]: edges) {
        cout << (double)pp[0][t] * pp[1][t] / (wp[0][t] * (wp[0][t] - 1) / 2); 
        t++;
    }
    return 0;
}