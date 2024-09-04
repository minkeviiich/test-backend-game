from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Player, LevelPrize, PlayerLevel
import csv
from django.http import HttpResponse

@login_required
def daily_login(request, player_id):
    player = get_object_or_404(
        Player, 
        id=player_id
    )
    if not player.first_login:
        player.first_login = timezone.now()
    player.daily_points += 10  # начисление баллов
    player.save()
    return render(
        request, 
        'gameapp/daily_login.html', {
        'player_name': player.user.username,
        'daily_points': player.daily_points
    })

def export_to_html(request):
    data = []
    for player_level in PlayerLevel.objects.select_related('player__user').all():
        if player_level.is_completed:
            prizes = ', '.join([
                lp.prize.title for lp in LevelPrize.objects.filter(
                    level=player_level.level
                )
            ])
            boosts = ', '.join([
                lp.boost.name for lp in LevelPrize.objects.filter(
                    level=player_level.level
                ) if lp.boost
            ])
        else:
            prizes = ''
            boosts = ''
        data.append({
            'player_id': player_level.player.id,
            'player_name': player_level.player.user.username,
            'level_title': player_level.level.title,
            'is_completed': player_level.is_completed,
            'prizes': prizes,
            'boosts': boosts
        })
    return render(request, 'gameapp/export_to_html.html', {'data': data})

def export_to_csv(request):
    response = HttpResponse(
        content_type='text/csv'
    )
    response['Content-Disposition'] = 'attachment; filename="player_levels.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Player ID', 'Player Name', 'Level Title', 'Completed', 'Prizes', 'Boosts'
    ])
    #итератор для обработки большого количества записей
    player_levels = PlayerLevel.objects.select_related('player__user').all().iterator()
    for player_level in player_levels:
        if player_level.is_completed:
            prizes = ', '.join([
                lp.prize.title for lp in LevelPrize.objects.filter(
                    level=player_level.level
                )
            ])
            boosts = ', '.join([
                lp.boost.name for lp in LevelPrize.objects.filter(
                    level=player_level.level
                ) if lp.boost
            ])
        else:
            prizes = ''
            boosts = ''
        writer.writerow([
            player_level.player.id,
            player_level.player.user.username,
            player_level.level.title,
            player_level.is_completed,
            prizes,
            boosts
        ])
    return response
