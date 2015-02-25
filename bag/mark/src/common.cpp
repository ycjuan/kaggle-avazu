#include <stdexcept>
#include <cstring>
#include <omp.h>

#include "common.h"

namespace {

int const kMaxLineSize = 1000000;

} //unamed namespace

Problem read_problem(std::string const path)
{
    if(path.empty())
        return Problem();
    Problem prob;

    FILE *f = open_c_file(path.c_str(), "r");
    char line[kMaxLineSize];

    uint64_t p = 0;
    prob.P.push_back(0);
    for(uint32_t i = 0; fgets(line, kMaxLineSize, f) != nullptr; ++i, ++prob.nr_instance)
    {
        char *y_char = strtok(line, " \t");
        float const y = (atoi(y_char)>0)? 1.0f : -1.0f;
        prob.Y.push_back(y);

        for(; ; ++p)
        {
            char *field_char = strtok(nullptr,":");
            char *idx_char = strtok(nullptr,":");
            char *value_char = strtok(nullptr," \t");
            if(field_char == nullptr || *field_char == '\n')
                break;
            uint32_t const field = static_cast<uint32_t>(atoi(field_char));
            uint32_t const idx = static_cast<uint32_t>(atoi(idx_char));
            float const value = static_cast<float>(atof(value_char));

            prob.nr_field = std::max(prob.nr_field, field);
            prob.nr_feature = std::max(prob.nr_feature, idx);

            prob.JFV.push_back(DNode(field-1, idx-1, value));
        }
        prob.P.push_back(p);
    }

    fclose(f);

    return prob;
}

FILE *open_c_file(std::string const &path, std::string const &mode)
{
    FILE *f = fopen(path.c_str(), mode.c_str());
    if(!f)
        throw std::runtime_error(std::string("cannot open ")+path);
    return f;
}

std::vector<std::string> 
argv_to_args(int const argc, char const * const * const argv)
{
    std::vector<std::string> args;
    for(int i = 1; i < argc; ++i)
        args.emplace_back(argv[i]);
    return args;
}

float predict(Problem const &prob, Model &model, 
    std::string const &output_path)
{
    FILE *f = nullptr;
    if(!output_path.empty())
        f = open_c_file(output_path, "w");

    double loss = 0;
    #pragma omp parallel for schedule(static) reduction(+:loss)
    for(uint32_t i = 0; i < prob.Y.size(); ++i)
    {
        float const y = prob.Y[i];

        float const t = wTx(prob, model, i);
        
        float const prob = 1/(1+static_cast<float>(exp(-t)));

        float const expnyt = static_cast<float>(exp(-y*t));

        loss += log(1+expnyt);

        if(f)
            fprintf(f, "%lf\n", prob);
    }

    if(f)
        fclose(f);

    return static_cast<float>(loss/static_cast<double>(prob.Y.size()));
}
