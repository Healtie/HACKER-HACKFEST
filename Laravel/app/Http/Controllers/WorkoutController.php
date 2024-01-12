<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;

class WorkoutController extends Controller
{
    public function getCaloriesToday($userId)
    {
        $totalCaloriesToday = DB::table('nutrition_results')
            ->where('userid', $userId)
            ->whereDate('created_at', today())
            ->sum('calories');
        return response()->json(['total_calories_today' => $totalCaloriesToday], 200);
    }

    public function getCaloriesThisWeek($userId)
    {
        $totalCaloriesThisWeek = DB::table('nutrition_results')
            ->where('userid', $userId)
            ->whereDate('created_at', '>=', today()->subDays(7))
            ->sum('calories');
        return response()->json(['total_calories_this_week' => $totalCaloriesThisWeek], 200);
    }

    public function getRecommendedWorkouts(Request $request)
    {
        $nowCalories = $request->input('Now', 0);
        $normalCalories = $request->input('normal', 0);

        $response = Http::get('http://34.171.82.75/workoutfor', [
            'Now' => $nowCalories,
            'normal' => $normalCalories,
        ]);
        if ($response->successful()) {
            $recommendedWorkouts = $response->json();
            return response()->json($recommendedWorkouts, 200);
        } else {
            return response()->json(['error' => 'Failed to fetch recommended workouts.'], 500);
        }
    }
}
