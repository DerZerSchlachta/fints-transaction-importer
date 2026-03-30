{
  description = "FinTS → hledger converter";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          pkgs.python312
          pkgs.python312Packages.pandas
          pkgs.python312Packages.fints
          pkgs.python312Packages.click
          pkgs.python312Packages.python-dateutil
          pkgs.python312Packages.python-dotenv
          pkgs.python312Packages.pyyaml
          pkgs.python312Packages.requests
          pkgs.python312Packages.fastapi
          pkgs.python312Packages.uvicorn
        ];

        shellHook = ''
          echo "📒 FinTS → hledger dev shell"
          echo "Python: $(python --version)"
        '';
      };
    };
}